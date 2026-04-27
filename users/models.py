from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Teacher specific fields (optional for students)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)

    # Approval system (VERY IMPORTANT)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Students auto-approved
        if self.role == 'student':
            self.is_approved = True

        super().save(*args, **kwargs)