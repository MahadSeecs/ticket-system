from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CLIENT = 'client'
    ROLE_PM = 'pm'
    ROLE_ENGINEER = 'engineer'
    ROLE_ADMIN = 'admin'

    #for better string readibility
    ROLE_CHOICES = [
    (ROLE_CLIENT, 'Client'),
    (ROLE_PM, 'Project Manager'),
    (ROLE_ENGINEER, 'Engineer'),
    (ROLE_ADMIN, 'Super Admin'),
]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.username} ({self.role})"