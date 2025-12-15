from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL
# Create your models here.


class Ticket(models.Model):
    STATUS_OPEN = "open"
    STATUS_ASSIGNED = "assigned"
    STATUS_RESOLVED = "resolved"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN
    )

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tickets"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    def __str__(self):
        return f"[{self.status}] {self.title}"
