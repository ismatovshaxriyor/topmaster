"""Jobs (buyurtmalar): client-posted work orders + lifecycle timeline.

NOTE: No payment processing. Price fields are informational only — they
record the budget a client offers; the platform never moves money.
"""
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from apps.common.models import TimeStampedModel


class JobStatus(models.TextChoices):
    OPEN = "open", "Ochiq"
    IN_PROGRESS = "in_progress", "Bajarilmoqda"
    AWAITING_CONFIRMATION = "awaiting_confirmation", "Tasdiqlash kutilmoqda"
    COMPLETED = "completed", "Yakunlandi"
    CANCELLED = "cancelled", "Bekor qilindi"


class PriceType(models.TextChoices):
    FIXED = "fixed", "Belgilangan narx"
    NEGOTIABLE = "negotiable", "Kelishiladi"


class WhenChoice(models.TextChoices):
    ASAP = "asap", "Imkon qadar tez"
    TODAY = "today", "Bugun"
    TOMORROW = "tomorrow", "Ertaga"
    THIS_WEEK = "this_week", "Shu hafta"
    EXACT = "exact", "Aniq sana"


class PaymentTiming(models.TextChoices):
    """Informational: when the client expects to pay the master directly."""

    ON_COMPLETION = "on_completion", "Ish yakunida"
    STAGED = "staged", "Bosqichma-bosqich"
    PREPAID = "prepaid", "Oldindan kelishilgan"


def job_image_upload_to(instance, filename):
    return f"jobs/job_{instance.job_id}/{filename}"


class Job(TimeStampedModel):
    """A work order posted by a client (mijoz)."""

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs"
    )
    category = models.ForeignKey(
        "catalog.Category", on_delete=models.SET_NULL, null=True, related_name="jobs"
    )
    city = models.ForeignKey(
        "catalog.City", on_delete=models.SET_NULL, null=True, related_name="jobs"
    )
    title = models.CharField(max_length=160)
    description = models.TextField()
    address = models.CharField(max_length=200, blank=True)

    price_type = models.CharField(
        max_length=12, choices=PriceType.choices, default=PriceType.FIXED
    )
    price_amount = models.PositiveIntegerField(
        null=True, blank=True, help_text="Mijoz taklif qilgan byudjet (soʻm) — faqat maʼlumot."
    )
    payment_timing = models.CharField(
        max_length=14, choices=PaymentTiming.choices, blank=True
    )

    when_choice = models.CharField(
        max_length=12, choices=WhenChoice.choices, default=WhenChoice.THIS_WEEK
    )
    due_date = models.DateField(null=True, blank=True)
    urgent = models.BooleanField(default=False)

    # Optional precise job location; nearby search falls back to the city.
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=22, choices=JobStatus.choices, default=JobStatus.OPEN
    )
    assigned_master = models.ForeignKey(
        "masters.MasterProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs",
    )
    proposals_count = models.PositiveIntegerField(default=0)

    # Postgres full-text index over title + description, kept current by a
    # post_save signal (apps.jobs.signals) and queried via ?q= on the board.
    search_vector = SearchVectorField(null=True, editable=False)

    class Meta:
        ordering = ("-urgent", "-created_at")
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["urgent"]),
            GinIndex(fields=["search_vector"], name="job_search_vector_gin"),
        ]

    def __str__(self):
        return self.title


class JobImage(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=job_image_upload_to)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return f"Image<{self.job_id}>"


class JobEvent(models.Model):
    """An immutable lifecycle event powering the order timeline."""

    class EventType(models.TextChoices):
        CREATED = "created", "Buyurtma joylandi"
        ACCEPTED = "accepted", "Usta qabul qildi"
        STARTED = "started", "Ish boshlandi"
        IN_PROGRESS = "in_progress", "Ish bajarilmoqda"
        AWAITING = "awaiting", "Tasdiqlash kutilmoqda"
        COMPLETED = "completed", "Ish yakunlandi"
        CANCELLED = "cancelled", "Bekor qilindi"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="events")
    type = models.CharField(max_length=14, choices=EventType.choices)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_events",
    )
    note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.job_id}:{self.type}"
