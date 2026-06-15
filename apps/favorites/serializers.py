"""Serializers for saved (favourite) masters."""
from rest_framework import serializers

from apps.masters.models import MasterProfile
from apps.masters.serializers import MasterSummarySerializer

from .models import SavedMaster


class SavedMasterSerializer(serializers.ModelSerializer):
    """Read representation: embeds the master summary card."""

    master = MasterSummarySerializer(read_only=True)

    class Meta:
        model = SavedMaster
        fields = ("id", "master", "created_at")


class SavedMasterCreateSerializer(serializers.ModelSerializer):
    """Write representation: master by primary key."""

    master = serializers.PrimaryKeyRelatedField(queryset=MasterProfile.objects.all())

    class Meta:
        model = SavedMaster
        fields = ("id", "master", "created_at")
        read_only_fields = ("id", "created_at")
