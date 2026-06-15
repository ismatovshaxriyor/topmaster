"""Serializers for reviews (sharhlar)."""
from rest_framework import serializers

from apps.accounts.serializers import UserSummarySerializer
from apps.jobs.models import Job, JobStatus

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Read representation of a review."""

    author = UserSummarySerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "author", "master", "rating", "text", "recommend", "created_at")
        read_only_fields = fields


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Create a review for a completed, assigned job authored by its client."""

    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())

    class Meta:
        model = Review
        fields = ("job", "rating", "text", "recommend")

    def validate(self, attrs):
        request = self.context["request"]
        job = attrs["job"]

        if job.client_id != request.user.id:
            raise serializers.ValidationError(
                {"job": "Faqat oʻz buyurtmangizga sharh qoldira olasiz."}
            )
        if job.status != JobStatus.COMPLETED:
            raise serializers.ValidationError(
                {"job": "Sharh faqat yakunlangan buyurtmaga qoldiriladi."}
            )
        if job.assigned_master_id is None:
            raise serializers.ValidationError(
                {"job": "Buyurtmaga usta biriktirilmagan."}
            )
        if Review.objects.filter(job=job).exists():
            raise serializers.ValidationError(
                {"job": "Bu buyurtmaga allaqachon sharh qoldirilgan."}
            )
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        job = validated_data["job"]
        return Review.objects.create(
            author=request.user,
            master=job.assigned_master,
            **validated_data,
        )
