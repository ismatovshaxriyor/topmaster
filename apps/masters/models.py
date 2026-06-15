"""Masters (ustalar): public profile, skills + prices, portfolio, verification."""
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import TimeStampedModel


class AvailabilityStatus(models.TextChoices):
    FREE = "free", "Bo'sh"
    BUSY = "busy", "Band"
    OFF = "off", "Faol emas"


def portfolio_upload_to(instance, filename):
    return f"portfolio/master_{instance.master_id}/{filename}"


def verification_upload_to(instance, filename):
    return f"verification/master_{instance.request.master_id}/{instance.doc_type}/{filename}"


class MasterProfile(TimeStampedModel):
    """Extends a User (role=usta) with marketplace-facing professional data.

    Aggregate fields (`rating_avg`, `reviews_count`, `views_count`) are
    denormalised and refreshed by signals / Celery tasks.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="master_profile",
    )
    bio = models.TextField(blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    min_price = models.PositiveIntegerField(
        default=0, help_text="Minimal buyurtma narxi (so'm)."
    )
    status = models.CharField(
        max_length=8, choices=AvailabilityStatus.choices, default=AvailabilityStatus.FREE
    )
    categories = models.ManyToManyField(
        "catalog.Category", related_name="masters", blank=True
    )

    is_top = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # Optional precise location; nearby search falls back to the user's city.
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-is_top", "-rating_avg", "-reviews_count")
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["is_verified"]),
            models.Index(fields=["is_top"]),
        ]

    def __str__(self):
        return f"Usta<{self.user.full_name or self.user.email}>"

    @property
    def spec(self) -> str:
        first = self.categories.first()
        return first.label if first else ""


class Skill(models.Model):
    """A specific service the master offers, with a price range (Ko'nikma)."""

    master = models.ForeignKey(
        MasterProfile, on_delete=models.CASCADE, related_name="skills"
    )
    category = models.ForeignKey(
        "catalog.Category", on_delete=models.SET_NULL, null=True, blank=True, related_name="skills"
    )
    title = models.CharField(max_length=120)
    price_min = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    price_max = models.PositiveIntegerField(null=True, blank=True)
    years = models.PositiveSmallIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.title


class PortfolioItem(TimeStampedModel):
    """A completed-work showcase entry (Ishlarim / Portfolio)."""

    master = models.ForeignKey(
        MasterProfile, on_delete=models.CASCADE, related_name="portfolio"
    )
    title = models.CharField(max_length=140)
    location = models.CharField(max_length=120, blank=True)
    completed_at = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=portfolio_upload_to, null=True, blank=True)
    category = models.ForeignKey(
        "catalog.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "-created_at")

    def __str__(self):
        return self.title


class VerificationRequest(TimeStampedModel):
    """KYC submission for a master (Profilni tasdiqlash)."""

    class Status(models.TextChoices):
        NONE = "none", "Boshlanmagan"
        PENDING = "pending", "Tekshiruvda"
        APPROVED = "approved", "Tasdiqlangan"
        REJECTED = "rejected", "Rad etilgan"

    master = models.OneToOneField(
        MasterProfile, on_delete=models.CASCADE, related_name="verification"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NONE)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verifications_reviewed",
    )
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Verification<{self.master_id}:{self.status}>"


class VerificationDocument(TimeStampedModel):
    """A single uploaded KYC document tied to a VerificationRequest."""

    class DocType(models.TextChoices):
        ID = "id", "Pasport / ID karta"
        SELFIE = "selfie", "Selfi tekshiruvi"
        DIPLOMA = "diploma", "Diplom / Sertifikat"
        ADDRESS = "address", "Manzil tasdig'i"

    class State(models.TextChoices):
        NONE = "none", "Yuklanmagan"
        UPLOADED = "uploaded", "Yuklandi"
        PENDING = "pending", "Tekshiruvda"
        VERIFIED = "verified", "Tasdiqlandi"
        REJECTED = "rejected", "Rad etildi"

    request = models.ForeignKey(
        VerificationRequest, on_delete=models.CASCADE, related_name="documents"
    )
    doc_type = models.CharField(max_length=10, choices=DocType.choices)
    file = models.FileField(upload_to=verification_upload_to, null=True, blank=True)
    required = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=State.choices, default=State.NONE)

    class Meta:
        unique_together = ("request", "doc_type")
        ordering = ("doc_type",)

    def __str__(self):
        return f"{self.get_doc_type_display()} ({self.state})"
