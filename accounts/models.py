from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('STAFF', 'Staff'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    # Explicitly redefine the inherited field to change its admin label:
    is_staff = models.BooleanField(
        'Admin status',
        default=False,
        help_text='Designates whether this user can log into the Admin Portal.'
    )

    def __str__(self):
        return f"{self.username} ({self.role} - {self.department})"