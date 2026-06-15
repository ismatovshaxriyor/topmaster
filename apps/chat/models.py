"""Real-time chat: conversations between two users and their messages."""
from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel


def message_attachment_upload_to(instance, filename):
    return f"chat/conversation_{instance.conversation_id}/{filename}"


class Conversation(TimeStampedModel):
    """A 1:1 thread. Optionally tied to a job order."""

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ConversationParticipant",
        related_name="conversations",
    )
    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conversations",
    )
    last_message = models.ForeignKey(
        "chat.Message",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        ordering = ("-updated_at",)

    def __str__(self):
        return f"Conversation<{self.pk}>"


class ConversationParticipant(models.Model):
    """Through model holding per-user unread state."""

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversation_memberships"
    )
    unread_count = models.PositiveIntegerField(default=0)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["conversation", "user"], name="uniq_conversation_participant"
            )
        ]

    def __str__(self):
        return f"{self.user_id}@{self.conversation_id}"


class Message(TimeStampedModel):
    class Type(models.TextChoices):
        TEXT = "text", "Matn"
        SYSTEM = "system", "Tizim"
        FILE = "file", "Fayl"

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages_sent",
        help_text="Null = tizim xabari.",
    )
    type = models.CharField(max_length=8, choices=Type.choices, default=Type.TEXT)
    text = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to=message_attachment_upload_to, null=True, blank=True
    )
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("created_at",)
        indexes = [models.Index(fields=["conversation", "created_at"])]

    def __str__(self):
        return f"Message<{self.pk}>"
