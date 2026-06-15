"""Saved / favourite masters (Saqlangan ustalar)."""
from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class SavedMaster(TimeStampedModel):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_masters"
    )
    master = models.ForeignKey(
        "masters.MasterProfile", on_delete=models.CASCADE, related_name="saved_by"
    )

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(fields=["client", "master"], name="uniq_saved_master")
        ]

    def __str__(self):
        return f"Saved<{self.client_id}:{self.master_id}>"
