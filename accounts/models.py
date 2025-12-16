from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'Client'
        PROJECT_MANAGER = 'project_manager', 'Project Manager'
        ENGINEER = 'engineer', 'Engineer'
        SUPER_ADMIN = 'super_admin', 'Super Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    

    def clean(self):
         if self.role == self.Role.SUPER_ADMIN and not self.is_superuser:
            raise ValidationError(
                {"role": "SUPER_ADMIN role requires is_superuser=True"}
            )
         
        #ensures always runs
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
