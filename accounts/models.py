from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

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
         

    ROLE_GROUP_MAP = {
    Role.CLIENT: "Clients",
    Role.ENGINEER: "Engineers",
    Role.PROJECT_MANAGER: "Project Managers",
    Role.SUPER_ADMIN: "Super Admins",
    }

    def assign_group_from_role(self):
        if self.role not in self.ROLE_GROUP_MAP:
            return
        group_name = self.ROLE_GROUP_MAP[self.role]
        group, _ = Group.objects.get_or_create(name=group_name)
        self.groups.clear()
        self.groups.add(group)

        #ensures always runs
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.assign_group_from_role()