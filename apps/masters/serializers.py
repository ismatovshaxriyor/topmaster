"""Serializers for the masters app.

Nested user/city/category data reuse the shared serializers from
apps.catalog / apps.accounts per the project serializer contract.
"""
from rest_framework import serializers

from apps.catalog.models import Category, City
from apps.catalog.serializers import CategorySerializer, CitySerializer

from .models import (
    MasterProfile,
    PortfolioItem,
    Skill,
    VerificationDocument,
    VerificationRequest,
)


class MasterSummarySerializer(serializers.ModelSerializer):
    """Compact master card for lists and cross-app embedding."""

    name = serializers.CharField(source="user.full_name", read_only=True)
    avatar = serializers.SerializerMethodField()
    spec = serializers.CharField(read_only=True)
    city = CitySerializer(source="user.city", read_only=True)
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = MasterProfile
        fields = (
            "id",
            "name",
            "avatar",
            "spec",
            "city",
            "experience_years",
            "rating_avg",
            "reviews_count",
            "min_price",
            "status",
            "is_verified",
            "is_top",
            "views_count",
            "distance_km",
        )

    def get_distance_km(self, obj) -> float | None:
        # Present only for nearby search (?lat&lng); otherwise null.
        value = getattr(obj, "distance_km", None)
        return round(value, 1) if value is not None else None

    def get_avatar(self, obj) -> str | None:
        avatar = getattr(obj.user, "avatar", None)
        if not avatar:
            return None
        request = self.context.get("request")
        url = avatar.url
        return request.build_absolute_uri(url) if request else url


class SkillSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )
    category_label = serializers.CharField(source="category.label", read_only=True)

    class Meta:
        model = Skill
        fields = (
            "id",
            "category",
            "category_label",
            "title",
            "price_min",
            "price_max",
            "years",
            "order",
        )


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = (
            "id",
            "title",
            "location",
            "completed_at",
            "image",
            "category",
            "featured",
            "order",
        )


class MasterDetailSerializer(MasterSummarySerializer):
    """Full master profile, including categories, skills and portfolio."""

    categories = CategorySerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    portfolio = PortfolioItemSerializer(many=True, read_only=True)
    recent_reviews = serializers.SerializerMethodField()

    class Meta(MasterSummarySerializer.Meta):
        fields = MasterSummarySerializer.Meta.fields + (
            "bio",
            "categories",
            "skills",
            "portfolio",
            "recent_reviews",
        )

    def get_recent_reviews(self, obj) -> list:
        from apps.reviews.models import Review

        reviews = (
            Review.objects.filter(master=obj)
            .select_related("author")
            .order_by("-created_at")[:5]
        )
        return [
            {
                "author_name": r.author.full_name or r.author.short_name,
                "rating": r.rating,
                "text": r.text,
                "created_at": r.created_at,
            }
            for r in reviews
        ]


class MasterProfileUpdateSerializer(serializers.ModelSerializer):
    """Master edits their own profile basics + categories."""

    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )

    class Meta:
        model = MasterProfile
        fields = (
            "bio",
            "experience_years",
            "min_price",
            "status",
            "categories",
            "latitude",
            "longitude",
        )


class AvailabilitySerializer(serializers.ModelSerializer):
    """Toggle availability status only."""

    class Meta:
        model = MasterProfile
        fields = ("status",)


class VerificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = ("id", "doc_type", "file", "required", "state")


class VerificationRequestSerializer(serializers.ModelSerializer):
    documents = VerificationDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = VerificationRequest
        fields = ("status", "submitted_at", "reviewed_at", "documents")


class OnboardingSerializer(serializers.Serializer):
    """First-run master setup: city, basics, categories and initial skills."""

    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), required=False, allow_null=True
    )
    bio = serializers.CharField(required=False, allow_blank=True)
    experience_years = serializers.IntegerField(required=False, min_value=0)
    min_price = serializers.IntegerField(required=False, min_value=0)
    category_keys = serializers.ListField(
        child=serializers.SlugField(), required=False
    )
    skills = serializers.ListField(child=serializers.DictField(), required=False)

    def update(self, instance: MasterProfile, validated_data):
        city = validated_data.get("city")
        if "city" in validated_data:
            instance.user.city = city
            instance.user.save(update_fields=["city"])

        for field in ("bio", "experience_years", "min_price"):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        category_keys = validated_data.get("category_keys")
        if category_keys is not None:
            categories = Category.objects.filter(key__in=category_keys)
            instance.categories.set(categories)

        skills = validated_data.get("skills")
        if skills:
            for s in skills:
                title = s.get("title")
                if not title:
                    continue
                Skill.objects.create(
                    master=instance,
                    title=title,
                    price_min=s.get("price_min") or 0,
                    price_max=s.get("price_max"),
                    years=s.get("years") or 0,
                )
        return instance


class DashboardStatsSerializer(serializers.Serializer):
    """Read-only aggregate numbers for the master dashboard."""

    total_orders = serializers.IntegerField(read_only=True)
    completed = serializers.IntegerField(read_only=True)
    rating_avg = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True
    )
    views = serializers.IntegerField(read_only=True)
    new_proposals = serializers.IntegerField(read_only=True)
