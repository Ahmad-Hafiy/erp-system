from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import PurchaseRequest
from .forms import PurchaseRequestForm

@login_required
def submit_purchase(request):
    if request.user.role not in ['STAFF', 'MANAGER']:
        messages.error(request, 'Only staff and managers can submit purchase requests.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()
            messages.success(request, 'Purchase request submitted successfully!')
            return redirect('dashboard')
    else:
        form = PurchaseRequestForm()
    return render(request, 'form_submit.html', {'form': form, 'title': 'Submit Purchase Request'})

@login_required
@require_POST
def review_purchase(request, pk, action):
    if request.user.role not in ['MANAGER', 'ADMIN']:
        raise PermissionDenied

    purchase = get_object_or_404(PurchaseRequest, pk=pk)

    if request.user.role == 'MANAGER':
        if purchase.user.department != request.user.department:
            raise PermissionDenied
        if purchase.user == request.user:
            messages.error(request, "You cannot review your own purchase request.")
            return redirect('dashboard')

    if purchase.status != 'PENDING':
        messages.warning(request, f"This request has already been marked as {purchase.status}.")
        return redirect('dashboard')

    purchase.status = 'APPROVED' if action == 'approve' else 'REJECTED'
    purchase.reviewed_by = request.user
    purchase.save()
    messages.success(request, f"Purchase request marked as {purchase.status}.")
    return redirect('dashboard')