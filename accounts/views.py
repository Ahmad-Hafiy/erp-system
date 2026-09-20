from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hr.models import LeaveRequest, ExpenseClaim, LeaveBalance
from procurement.models import PurchaseRequest

@login_required
def dashboard(request):
    user = request.user

    # Fetch personal balance and requests for the logged-in user
    balance, _ = LeaveBalance.objects.get_or_create(user=user)
    leaves = LeaveRequest.objects.filter(user=user).order_by('-created_at')
    expenses = ExpenseClaim.objects.filter(user=user).order_by('-created_at')
    purchases = PurchaseRequest.objects.filter(user=user).order_by('-created_at')

    # Staff: view only personal workspace
    if user.role == 'STAFF':
        return render(request, 'dashboard_staff.html', {
            'balance': balance,
            'leaves': leaves,
            'expenses': expenses,
            'purchases': purchases,
        })

    # Manager: pending requests from their department (excluding their own requests)
    elif user.role == 'MANAGER':
        dept_users = user.department.user_set.exclude(pk=user.pk) if user.department else []
        team_leaves = LeaveRequest.objects.filter(user__in=dept_users, status='PENDING').order_by('-created_at')
        team_expenses = ExpenseClaim.objects.filter(user__in=dept_users, status='PENDING').order_by('-created_at')
        team_purchases = PurchaseRequest.objects.filter(user__in=dept_users, status='PENDING').order_by('-created_at')

        return render(request, 'dashboard_manager.html', {
            'balance': balance,
            'leaves': leaves,
            'expenses': expenses,
            'purchases': purchases,
            'team_leaves': team_leaves,
            'team_expenses': team_expenses,
            'team_purchases': team_purchases,
            'is_admin': False,
        })

    # Admin: global view of all pending requests across all departments
    else:
        team_leaves = LeaveRequest.objects.filter(status='PENDING').order_by('-created_at')
        team_expenses = ExpenseClaim.objects.filter(status='PENDING').order_by('-created_at')
        team_purchases = PurchaseRequest.objects.filter(status='PENDING').order_by('-created_at')

        return render(request, 'dashboard_manager.html', {
            'balance': balance,
            'leaves': leaves,
            'expenses': expenses,
            'purchases': purchases,
            'team_leaves': team_leaves,
            'team_expenses': team_expenses,
            'team_purchases': team_purchases,
            'is_admin': True,
        })