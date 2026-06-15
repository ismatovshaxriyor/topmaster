"""Serializers for the jobs (buyurtmalar) app."""
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.accounts.serializers import UserSummarySerializer
from apps.catalog.models import Category, City
from apps.catalog.serializers import CategorySerializer, CitySerializer
from apps.masters.serializers import MasterSummarySerializer

from .models import Job, JobEvent, JobImage


class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobImage
        fields = ("id", "image", "order")


class JobEventSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    actor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = JobEvent
        fields = ("id", "type", "type_display", "note", "actor", "created_at")


class JobListSerializer(serializers.ModelSerializer):
    """Card representation for the job board."""

    category = CategorySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    client = UserSummarySerializer(read_only=True)
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "category",
            "city",
            "price_type",
            "price_amount",
            "when_choice",
            "due_date",
            "urgent",
            "status",
            "status_display",
            "proposals_count",
            "created_at",
            "client",
            "distance_km",
        )

    def get_distance_km(self, obj) -> float | None:
        # Present only for nearby search (?lat&lng); otherwise null.
        value = getattr(obj, "distance_km", None)
        return round(value, 1) if value is not None else None


class JobDetailSerializer(JobListSerializer):
    images = JobImageSerializer(many=True, read_only=True)
    events = serializers.SerializerMethodField()
    assigned_master = MasterSummarySerializer(read_only=True)

    class Meta(JobListSerializer.Meta):
        fields = JobListSerializer.Meta.fields + (
            "description",
            "address",
            "payment_timing",
            "images",
            "events",
            "assigned_master",
        )

    @extend_schema_field(JobEventSerializer(many=True))
    def get_events(self, obj):
        events = obj.events.all().order_by("created_at")
        return JobEventSerializer(events, many=True).data


class JobCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Job
        fields = (
            "id",
            "category",
            "city",
            "title",
            "description",
            "address",
            "price_type",
            "price_amount",
            "payment_timing",
            "when_choice",
            "due_date",
            "urgent",
            "latitude",
            "longitude",
        )
