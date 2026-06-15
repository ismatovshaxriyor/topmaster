"""Serializers for the help center (FAQ topics/entries + support chat)."""
from rest_framework import serializers

from apps.support.models import Faq, FaqTopic, SupportMessage, SupportThread


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ("id", "question", "answer", "order")


class FaqTopicSerializer(serializers.ModelSerializer):
    faqs = FaqSerializer(many=True, read_only=True)

    class Meta:
        model = FaqTopic
        fields = ("id", "key", "label", "icon", "faqs")


class SupportMessageSerializer(serializers.ModelSerializer):
    """One message in a support thread. `is_staff` marks support-team replies."""

    attachment = serializers.FileField(use_url=True, read_only=True)

    class Meta:
        model = SupportMessage
        fields = ("id", "is_staff", "text", "attachment", "read_at", "created_at")
        read_only_fields = fields


class SupportThreadSerializer(serializers.ModelSerializer):
    last_message = SupportMessageSerializer(read_only=True)

    class Meta:
        model = SupportThread
        fields = (
            "id",
            "subject",
            "status",
            "user_unread",
            "last_message",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class SupportSendSerializer(serializers.Serializer):
    """Input for a user posting a message to support."""

    text = serializers.CharField(allow_blank=False, trim_whitespace=True)
    subject = serializers.CharField(required=False, allow_blank=True, max_length=160)
