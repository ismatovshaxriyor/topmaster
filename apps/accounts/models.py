"""Accounts: custom User, per-user settings, and FCM devices."""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.common.models import TimeStampedModel

from .managers import UserManager


class Role(models.TextChoices):
    CLIENT = "mijoz", "Mijoz"
    MASTER = "usta", "Usta"


def avatar_upload_to(instance, filename):
    return f"avatars/user_{instance.pk or 'new'}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    """Email-based user. `role` decides client vs master capabilities.

    A user with role=usta also owns a `master_profile` (apps.masters).
    """

    email = models.EmailField("email", unique=True)
    full_name = models.CharField("to'liq ism", max_length=150, blank=True)
    phone = models.CharField("telefon", max_length=32, blank=True)
    city = models.ForeignKey(
        "catalog.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    avatar = models.ImageField(upload_to=avatar_upload_to, null=True, blank=True)

    # Client-level verification (phone/identity confirmed). Master verification
    # is tracked separately in apps.masters.VerificationRequest.
    is_verified = models.BooleanField(default=False)

    # Email ownership confirmed via the post-registration code flow. New sign-ups
    # start False; the verification code lives in the cache (15-min TTL).
    email_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return self.full_name or self.email

    @property
    def is_client(self) -> bool:
        return self.role == Role.CLIENT

    @property
    def is_master(self) -> bool:
        return self.role == Role.MASTER

    @property
    def short_name(self) -> str:
        return (self.full_name or self.email).split(" ")[0]


class UserSettings(TimeStampedModel):
    """Notification + appearance preferences (Account → Sozlamalar)."""

    class Language(models.TextChoices):
        UZ = "uz", "O'zbekcha"
        RU = "ru", "Русский"
        EN = "en", "English"

    class Theme(models.TextChoices):
        LIGHT = "light", "Kunduzgi"
        DARK = "dark", "Tungi"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    notif_push = models.BooleanField(default=True)
    notif_email = models.BooleanField(default=False)
    notif_sms = models.BooleanField(default=True)
    notif_promo = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.UZ)
    theme = models.CharField(max_length=6, choices=Theme.choices, default=Theme.LIGHT)
    twofa = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings<{self.user_id}>"


class Device(TimeStampedModel):
    """Registered FCM device token for push delivery."""

    class Platform(models.TextChoices):
        ANDROID = "android", "Android"
        IOS = "ios", "iOS"
        WEB = "web", "Web"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    registration_id = models.TextField(unique=True)
    platform = models.CharField(max_length=10, choices=Platform.choices, default=Platform.ANDROID)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.get_platform_display()} device<{self.user_id}>"
