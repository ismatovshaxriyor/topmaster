"""In-app notifications. Delivered live over WebSocket + (optionally) FCM push."""
from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class NotificationType(models.TextChoices):
    ORDER = "order", "Buyurtma"
    ACCEPTED = "accepted", "Qabul qilindi"
    REJECTED = "rejected", "Rad etildi"
    CHAT = "chat", "Xabar"
    SYSTEM = "system", "Tizim"


class Notification(TimeStampedModel):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    type = models.CharField(max_length=10, choices=NotificationType.choices)
    title = models.CharField(max_length=160)
    body = models.CharField(max_length=400, blank=True)
    # Arbitrary related ids for deep-linking, e.g. {"job_id": 12, "master_id": 3}.
    data = models.JSONField(default=dict, blank=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["recipient", "read", "-created_at"])]

    def __str__(self):
        return f"{self.type}:{self.title}"
