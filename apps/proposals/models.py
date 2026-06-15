"""Proposals (takliflar): a master applies to a client's job order."""
from django.db import models

from apps.common.models import TimeStampedModel


class Proposal(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        ACCEPTED = "accepted", "Qabul qilindi"
        REJECTED = "rejected", "Rad etildi"
        WITHDRAWN = "withdrawn", "Qaytarib olindi"

    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name="proposals")
    master = models.ForeignKey(
        "masters.MasterProfile", on_delete=models.CASCADE, related_name="proposals"
    )
    message = models.TextField(blank=True)
    proposed_price = models.PositiveIntegerField(
        null=True, blank=True, help_text="Usta taklif qilgan narx (so'm) — faqat maʼlumot."
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(fields=["job", "master"], name="uniq_proposal_per_master")
        ]

    def __str__(self):
        return f"Taklif<{self.job_id}:{self.master_id}:{self.status}>"
