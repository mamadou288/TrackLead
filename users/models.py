from django.db import models
from django.contrib.auth.models import AbstractUser
from company.models import Company
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('sales', 'Commercial'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales')
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    

class Invitation(models.Model):
    ROLE_CHOICES = [
        ('sales', 'Commercial'),
        ('manager', 'Manager'),
    ]

    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.company.name} ({self.role})"
