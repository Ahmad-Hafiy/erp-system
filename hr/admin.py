from django.contrib import admin
from .models import LeaveBalance, LeaveRequest, ExpenseClaim

admin.site.register(LeaveBalance)
admin.site.register(LeaveRequest)
admin.site.register(ExpenseClaim)