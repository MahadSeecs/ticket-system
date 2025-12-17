from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


User = settings.AUTH_USER_MODEL


class Ticket(models.Model):

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        ASSIGNED = "assigned", "Assigned"
        RESOLVED = "resolved", "Resolved"

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tickets",
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"
    

    def clean(self):
        #assigning if status is OPEN
        if self.assigned_to and self.status != self.Status.OPEN:
            raise ValidationError(
                "Ticket can only be assigned if status is OPEN."
            )

        #resolving if status is ASSIGNED
        if self.status == self.Status.RESOLVED and not self.assigned_to:
            raise ValidationError(
                "Ticket must be assigned before it can be resolved."
            )

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)
