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
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'ADMIN',
                'department': eng,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('AdminPass2026!')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created Admin: admin / AdminPass2026!'))
        else:
            self.stdout.write('Admin account already exists.')

        # 3. Manager User
        manager_user, created = User.objects.get_or_create(
            username='manager_dan',
            defaults={
                'email': 'dan@example.com',
                'role': 'MANAGER',
                'department': eng,
                'is_staff': False,
            }
        )
        if created:
            manager_user.set_password('ErpTest2026!')
            manager_user.save()
            self.stdout.write(self.style.SUCCESS('Created Manager: manager_dan / ErpTest2026!'))
        else:
            self.stdout.write('Manager account already exists.')
        
        LeaveBalance.objects.get_or_create(user=manager_user, defaults={'remaining_days': 20})

        # 4. Staff User
        staff_user, created = User.objects.get_or_create(
            username='staff_alice',
            defaults={
                'email': 'alice@example.com',
                'role': 'STAFF',
                'department': eng,
                'is_staff': False,
            }
        )
        if created:
            staff_user.set_password('ErpTest2026!')
            staff_user.save()
            self.stdout.write(self.style.SUCCESS('Created Staff: staff_alice / ErpTest2026!'))
        else:
            self.stdout.write('Staff account already exists.')
            
        LeaveBalance.objects.get_or_create(user=staff_user, defaults={'remaining_days': 15})

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))