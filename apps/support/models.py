"""Help center (Yordam markazi): FAQ topics/entries + support chat."""
from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


class FaqTopic(models.Model):
    key = models.SlugField(max_length=40, unique=True)
    label = models.CharField(max_length=80)
    icon = models.CharField(max_length=40, default="help-circle")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "label")

    def __str__(self):
        return self.label


class Faq(models.Model):
    topic = models.ForeignKey(FaqTopic, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return self.question


# ── Support chat (yordam suhbati) ─────────────────────────────────
def support_attachment_upload_to(instance, filename):
    return f"support/thread_{instance.thread_id}/{filename}"


class SupportThread(TimeStampedModel):
    """A user's conversation with the support team, handled from the admin."""

    class Status(models.TextChoices):
        OPEN = "open", "Ochiq"
        PENDING = "pending", "Javob kutilmoqda"
        RESOLVED = "resolved", "Hal qilindi"
        CLOSED = "closed", "Yopilgan"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="support_threads"
    )
    subject = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    assigned_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_support_threads",
        limit_choices_to={"is_staff": True},
    )
    # Denormalised unread counters per side.
    user_unread = models.PositiveIntegerField(default=0)   # staff replies unseen by user
    staff_unread = models.PositiveIntegerField(default=0)  # user messages unseen by staff
    last_message = models.ForeignKey(
        "support.SupportMessage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        ordering = ("-updated_at",)
        indexes = [models.Index(fields=["status", "-updated_at"])]

    def __str__(self):
        return f"Support<{self.user_id}:{self.status}>"

    @property
    def is_active(self) -> bool:
        return self.status in (self.Status.OPEN, self.Status.PENDING)


class SupportMessage(TimeStampedModel):
    thread = models.ForeignKey(
        SupportThread, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="support_messages",
        help_text="Null = tizim xabari.",
    )
    # True = reply from the support team (staff), False = from the user.
    is_staff = models.BooleanField(default=False)
    text = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to=support_attachment_upload_to, null=True, blank=True
    )
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("created_at",)
        indexes = [models.Index(fields=["thread", "created_at"])]

    def __str__(self):
        who = "Support" if self.is_staff else "User"
        return f"{who} msg<{self.thread_id}>"
