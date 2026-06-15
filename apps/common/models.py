"""Shared abstract models."""
from django.db import models


class TimeStampedModel(models.Model):
    """Adds self-managed `created_at` / `updated_at` fields."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class BaseModel(TimeStampedModel):
    """Default base for domain models. Extend per app as needed."""

    class Meta(TimeStampedModel.Meta):
        abstract = True
