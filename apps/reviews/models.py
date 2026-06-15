"""Reviews (sharhlar): a client rates a master after a completed job."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class Review(TimeStampedModel):
    job = models.OneToOneField(
        "jobs.Job", on_delete=models.CASCADE, related_name="review"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews_written"
    )
    master = models.ForeignKey(
        "masters.MasterProfile", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(blank=True)
    recommend = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["master", "-created_at"])]

    def __str__(self):
        return f"Sharh<{self.master_id}:{self.rating}★>"
