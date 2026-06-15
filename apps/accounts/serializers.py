"""Accounts serializers: registration, auth, profile, settings, devices."""
from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.catalog.models import City
from apps.catalog.serializers import CitySerializer

from .models import Device, Role, UserSettings

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Create a new account; provisions master profile + KYC rows for ustalar."""

    password = serializers.CharField(write_only=True)
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ("email", "password", "full_name", "phone", "city", "role")

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        role = validated_data.get("role", Role.CLIENT)
        user = User.objects.create_user(password=password, **validated_data)

        if role == Role.MASTER:
            # Lazy import to keep accounts -> masters import direction clean.
            from apps.masters.models import (
                MasterProfile,
                VerificationDocument,
                VerificationRequest,
            )

            profile = MasterProfile.objects.create(user=user)
            request = VerificationRequest.objects.create(
                master=profile, status=VerificationRequest.Status.NONE
            )
            DocType = VerificationDocument.DocType
            State = VerificationDocument.State
            defaults = [
                (DocType.ID, True),
                (DocType.SELFIE, True),
                (DocType.DIPLOMA, False),
                (DocType.ADDRESS, False),
            ]
            VerificationDocument.objects.bulk_create(
                [
                    VerificationDocument(
                        request=request,
                        doc_type=doc_type,
                        required=required,
                        state=State.NONE,
                    )
                    for doc_type, required in defaults
                ]
            )
        return user


class UserSummarySerializer(serializers.ModelSerializer):
    """Compact, public-safe user representation reused across apps.

    Intentionally excludes contact details (email/phone): this serializer is
    embedded in AllowAny endpoints (reviews) and in the job board card seen by
    every master. Private contact data lives only in MeSerializer.
    """

    avatar = serializers.ImageField(use_url=True, read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "role",
            "is_verified",
            "avatar",
            "city",
        )
        read_only_fields = fields


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = (
            "notif_push",
            "notif_email",
            "notif_sms",
            "notif_promo",
            "language",
            "theme",
            "twofa",
        )


class MeSerializer(serializers.ModelSerializer):
    """Authenticated user's own profile (read + update)."""

    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        source="city",
        queryset=City.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    avatar = serializers.ImageField(use_url=True, required=False, allow_null=True)
    has_master_profile = serializers.SerializerMethodField()
    settings = UserSettingsSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "role",
            "is_verified",
            "email_verified",
            "avatar",
            "city",
            "city_id",
            "is_master",
            "has_master_profile",
            "settings",
        )
        read_only_fields = (
            "id",
            "email",
            "role",
            "is_verified",
            "email_verified",
            "is_master",
        )

    def get_has_master_profile(self, obj) -> bool:
        return hasattr(obj, "master_profile")


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("id", "registration_id", "platform", "active")
        read_only_fields = ("id",)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Joriy parol notoʻgʻri.")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value, self.context["request"].user)
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Validate a reset link (uid + token) and set the new password."""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        try:
            pk = force_str(urlsafe_base64_decode(attrs["uid"]))
            user = User.objects.get(pk=pk, is_active=True)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            # Same generic error for bad uid / token — never reveal which.
            raise serializers.ValidationError(
                {"token": "Havola yaroqsiz yoki muddati oʻtgan."}
            ) from None
        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError(
                {"token": "Havola yaroqsiz yoki muddati oʻtgan."}
            )
        password_validation.validate_password(attrs["new_password"], user)
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds the authenticated user payload to the token response."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSummarySerializer(self.user).data
        return data
