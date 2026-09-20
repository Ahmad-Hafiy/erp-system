from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('ERP Details', {'fields': ('role', 'department')}),
    )
    list_display = ['username', 'email', 'role', 'department', 'is_staff']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)