from django.core.management.base import BaseCommand
from accounts.models import User, Department
from hr.models import LeaveBalance

class Command(BaseCommand):
    help = 'Seeds initial test data (Departments, Users, and Leave Balances)'

    def handle(self, *args, **kwargs):
        # 1. Departments
        eng, _ = Department.objects.get_or_create(name='Engineering')
        sales, _ = Department.objects.get_or_create(name='Sales')

        # 2. Admin User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='AdminPass2026!',
                role='ADMIN',
                department=eng
            )
            self.stdout.write(self.style.SUCCESS('Created Admin: admin / AdminPass2026!'))
        else:
            self.stdout.write('Admin account already exists.')

        # 3. Manager User
        if not User.objects.filter(username='manager_dan').exists():
            manager = User.objects.create_user(
                username='manager_dan',
                email='dan@example.com',
                password='ErpTest2026!',
                role='MANAGER',
                department=eng
            )
            LeaveBalance.objects.get_or_create(user=manager, defaults={'annual_leave_balance': 20})
            self.stdout.write(self.style.SUCCESS('Created Manager: manager_dan / ErpTest2026!'))
        else:
            self.stdout.write('Manager account already exists.')

        # 4. Staff User
        if not User.objects.filter(username='staff_alice').exists():
            staff = User.objects.create_user(
                username='staff_alice',
                email='alice@example.com',
                password='ErpTest2026!',
                role='STAFF',
                department=eng
            )
            LeaveBalance.objects.get_or_create(user=staff, defaults={'annual_leave_balance': 15})
            self.stdout.write(self.style.SUCCESS('Created Staff: staff_alice / ErpTest2026!'))
        else:
            self.stdout.write('Staff account already exists.')

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))