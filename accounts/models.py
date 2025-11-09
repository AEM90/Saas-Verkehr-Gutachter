from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ("superadmin", "Superadmin"),
    ("admin", "Admin"),
    ("engineer", "Engineer"),
]

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="engineer")
    company = models.ForeignKey("companies.Company", null=True, blank=True, on_delete=models.SET_NULL, related_name="users")

    def is_superadmin(self):
        return self.role == "superadmin"