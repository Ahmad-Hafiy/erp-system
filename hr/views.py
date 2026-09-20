from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db import transaction
from .models import LeaveRequest, ExpenseClaim, LeaveBalance
from .forms import LeaveRequestForm, ExpenseClaimForm

@login_required
def submit_leave(request):
    if request.user.role not in ['STAFF', 'MANAGER']:
        messages.error(request, 'Only staff and managers can submit leave requests.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, user=request.user)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('dashboard')
    else:
        form = LeaveRequestForm(user=request.user)
    return render(request, 'form_submit.html', {'form': form, 'title': 'Submit Leave Request'})

@login_required
def submit_expense(request):
    if request.user.role not in ['STAFF', 'MANAGER']:
        messages.error(request, 'Only staff and managers can submit expense claims.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ExpenseClaimForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense claim submitted successfully!')
            return redirect('dashboard')
    else:
        form = ExpenseClaimForm()
    return render(request, 'form_submit.html', {'form': form, 'title': 'Submit Expense Claim'})

@login_required
@require_POST
def review_leave(request, pk, action):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        raise PermissionDenied

    leave = get_object_or_404(LeaveRequest, pk=pk)

    # Prevent managers from reviewing outside their department or approving their own requests
    if request.user.role == 'MANAGER':
        if leave.user.department != request.user.department:
            raise PermissionDenied
        if leave.user == request.user:
            messages.error(request, "You cannot review your own leave request.")
            return redirect('dashboard')

    # Guard: only review pending items to prevent duplicate deductions
    if leave.status != 'PENDING':
        messages.warning(request, f"This request has already been marked as {leave.status}.")
        return redirect('dashboard')

    if action == 'approve':
        with transaction.atomic():
            balance, _ = LeaveBalance.objects.get_or_create(user=leave.user)
            if balance.remaining_days >= leave.days_requested:
                balance.remaining_days -= leave.days_requested
                balance.save()
                leave.status = 'APPROVED'
            else:
                messages.error(request, f"Insufficient leave balance for {leave.user.username}.")
                return redirect('dashboard')
    elif action == 'reject':
        leave.status = 'REJECTED'

    leave.reviewed_by = request.user
    leave.save()
    messages.success(request, f"Leave request marked as {leave.status}.")
    return redirect('dashboard')

@login_required
@require_POST
def review_expense(request, pk, action):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        raise PermissionDenied

    expense = get_object_or_404(ExpenseClaim, pk=pk)

    if request.user.role == 'MANAGER':
        if expense.user.department != request.user.department:
            raise PermissionDenied
        if expense.user == request.user:
            messages.error(request, "You cannot review your own expense claim.")
            return redirect('dashboard')

    if expense.status != 'PENDING':
        messages.warning(request, f"This expense claim has already been marked as {expense.status}.")
        return redirect('dashboard')

    expense.status = 'APPROVED' if action == 'approve' else 'REJECTED'
    expense.reviewed_by = request.user
    expense.save()
    messages.success(request, f"Expense claim marked as {expense.status}.")
    return redirect('dashboard')