"""Serializers for in-app notifications."""
from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Read-only representation of a notification."""

    type_display = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = Notification
        fields = ("id", "type", "type_display", "title", "body", "data", "read", "created_at")
        read_only_fields = fields
