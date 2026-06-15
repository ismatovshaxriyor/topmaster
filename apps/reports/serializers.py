"""Report serializer: friendly target_type/target_id in, generic FK stored."""
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from rest_framework import serializers

from .models import Report

# Friendly API key -> (app_label, model). Only these objects are reportable;
# anything else is rejected so reports can't point at arbitrary tables.
REPORTABLE = {
    "master": ("masters", "masterprofile"),
    "job": ("jobs", "job"),
    "review": ("reviews", "review"),
    "user": ("accounts", "user"),
}


class ReportSerializer(serializers.ModelSerializer):
    target_type = serializers.ChoiceField(
        choices=list(REPORTABLE.keys()), write_only=True
    )
    target_id = serializers.IntegerField(write_only=True, min_value=1)
    target_label = serializers.SerializerMethodField(read_only=True)
    reason_display = serializers.CharField(source="get_reason_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Report
        fields = (
            "id",
            "target_type",
            "target_id",
            "target_label",
            "reason",
            "reason_display",
            "description",
            "status",
            "status_display",
            "created_at",
        )
        read_only_fields = ("id", "status", "created_at")

    def get_target_label(self, obj) -> str:
        target = obj.target
        return str(target) if target is not None else f"{obj.content_type.model} #{obj.object_id}"

    def validate(self, attrs):
        target_type = attrs.pop("target_type")
        target_id = attrs.pop("target_id")
        app_label, model = REPORTABLE[target_type]
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(
                {"target_type": "Noto'g'ri obyekt turi."}
            ) from None
        model_cls = ct.model_class()
        if model_cls is None or not model_cls.objects.filter(pk=target_id).exists():
            raise serializers.ValidationError({"target_id": "Obyekt topilmadi."})
        attrs["content_type"] = ct
        attrs["object_id"] = target_id
        return attrs

    def create(self, validated_data):
        validated_data["reporter"] = self.context["request"].user
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Siz bu obyekt ustidan allaqachon shikoyat qilgansiz."
            ) from None
