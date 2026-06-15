"""Proposal serializers (takliflar)."""
from rest_framework import serializers

from apps.masters.serializers import MasterSummarySerializer

from .models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    master = MasterSummarySerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Proposal
        fields = (
            "id",
            "job",
            "job_title",
            "master",
            "message",
            "proposed_price",
            "status",
            "status_display",
            "created_at",
            "responded_at",
        )
        read_only_fields = fields


class ProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ("job", "message", "proposed_price")
