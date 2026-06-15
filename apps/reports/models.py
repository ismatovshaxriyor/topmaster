"""User-submitted abuse reports against any reportable object.

Generic (ContentType) so a single model covers masters, jobs, reviews and
users. Moderators triage them from the Django admin; there is no money or
payment dimension here — reports are purely a trust-and-safety signal.
"""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.common.models import TimeStampedModel


class Report(TimeStampedModel):
    class Reason(models.TextChoices):
        SPAM = "spam", "Spam / reklama"
        FRAUD = "fraud", "Firibgarlik"
        INAPPROPRIATE = "inappropriate", "Nomaqbul kontent"
        FAKE = "fake", "Soxta profil / maʼlumot"
        ABUSE = "abuse", "Haqorat / tahdid"
        OTHER = "other", "Boshqa"

    class Status(models.TextChoices):
        OPEN = "open", "Yangi"
        REVIEWING = "reviewing", "Ko'rib chiqilmoqda"
        RESOLVED = "resolved", "Hal qilindi"
        DISMISSED = "dismissed", "Rad etildi"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_made",
    )
    # Generic target (master / job / review / user / …).
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    reason = models.CharField(max_length=16, choices=Reason.choices)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.OPEN, db_index=True
    )
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_handled",
    )
    resolution_note = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["status"]),
        ]
        constraints = [
            # One report per user per object — re-reporting is a no-op (spam guard).
            models.UniqueConstraint(
                fields=["reporter", "content_type", "object_id"],
                name="unique_report_per_user_target",
            )
        ]

    def __str__(self):
        return f"Report<{self.content_type.model}#{self.object_id}:{self.reason}>"
