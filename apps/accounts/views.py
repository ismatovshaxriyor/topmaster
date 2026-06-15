"""Accounts views: auth, profile, settings, password, devices."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.common.throttles import (
    LoginRateThrottle,
    PasswordResetRateThrottle,
    RegisterRateThrottle,
)

from .models import Device
from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    DeviceSerializer,
    MeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSettingsSerializer,
    UserSummarySerializer,
)

User = get_user_model()


@extend_schema(tags=["Auth & Accounts"])
class RegisterView(CreateAPIView):
    """Public self-registration for clients and masters."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [RegisterRateThrottle]

    @extend_schema(responses={201: UserSummarySerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSummarySerializer(user).data, status=status.HTTP_201_CREATED
        )


@extend_schema(tags=["Auth & Accounts"])
class LoginView(TokenObtainPairView):
    """Obtain JWT pair; response also embeds the user summary."""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]


@extend_schema(tags=["Auth & Accounts"])
class LogoutView(APIView):
    """Blacklist the supplied refresh token."""

    serializer_class = None

    @extend_schema(
        request=inline_serializer(
            name="LogoutRequest",
            fields={"refresh": serializers.CharField()},
        ),
        responses={205: OpenApiResponse(description="Tizimdan chiqildi.")},
    )
    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response(
                {"detail": "Refresh token majburiy."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            return Response(
                {"detail": "Token yaroqsiz yoki muddati oʻtgan."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_205_RESET_CONTENT)


@extend_schema(tags=["Auth & Accounts"])
class MeView(RetrieveUpdateAPIView):
    """Read / update the authenticated user's own profile."""

    serializer_class = MeSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Auth & Accounts"])
class SettingsView(RetrieveUpdateAPIView):
    """Read / update the authenticated user's preferences."""

    serializer_class = UserSettingsSerializer
    queryset = User.objects.all()

    def get_object(self):
        from .models import UserSettings

        obj, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return obj


@extend_schema(tags=["Auth & Accounts"])
class ChangePasswordView(APIView):
    """Change the current user's password (requires the old one)."""

    serializer_class = ChangePasswordSerializer

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: OpenApiResponse(description="Parol yangilandi.")},
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Parol muvaffaqiyatli yangilandi."})


@extend_schema(tags=["Auth & Accounts"])
class PasswordResetRequestView(APIView):
    """Request a password reset link. Always returns 200 (no email leak)."""

    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: OpenApiResponse(description="Soʻrov qabul qilindi.")},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user is not None:
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.encoding import force_bytes
            from django.utils.http import urlsafe_base64_encode

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_PASSWORD_RESET_URL}?uid={uid}&token={token}"
            send_mail(
                subject="TopMaster: parolni tiklash",
                message=(
                    "Assalomu alaykum!\n\n"
                    "Parolingizni tiklash uchun quyidagi havolani oching:\n"
                    f"{reset_link}\n\n"
                    "Yoki ilovaga ushbu maʼlumotlarni kiriting:\n"
                    f"uid: {uid}\n"
                    f"token: {token}\n\n"
                    "Havola cheklangan muddat amal qiladi. Agar bu soʻrovni siz "
                    "yubormagan boʻlsangiz, xabarni eʼtiborsiz qoldiring."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
        return Response(
            {"detail": "Agar hisob mavjud boʻlsa, koʻrsatmalar yuborildi."}
        )


@extend_schema(tags=["Auth & Accounts"])
class PasswordResetConfirmView(APIView):
    """Complete a password reset: verify uid+token and set the new password."""

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: OpenApiResponse(description="Parol oʻzgartirildi.")},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Security: a password reset invalidates every existing session by
        # blacklisting the user's outstanding refresh tokens.
        try:
            from rest_framework_simplejwt.token_blacklist.models import (
                BlacklistedToken,
                OutstandingToken,
            )

            for outstanding in OutstandingToken.objects.filter(user=user):
                BlacklistedToken.objects.get_or_create(token=outstanding)
        except Exception:  # blacklist app issues must not block the reset
            pass
        return Response({"detail": "Parol muvaffaqiyatli oʻzgartirildi."})


@extend_schema(tags=["Auth & Accounts"])
class DeviceViewSet(viewsets.ModelViewSet):
    """Manage the user's FCM device tokens (upsert by registration_id)."""

    serializer_class = DeviceSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Device.objects.none()
        return self.request.user.devices.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        reg_id = data["registration_id"]
        # Never let one user silently take over a token already owned by another.
        owner = (
            Device.objects.filter(registration_id=reg_id)
            .exclude(user=request.user)
            .first()
        )
        if owner is not None:
            return Response(
                {"detail": "Bu qurilma tokeni boshqa hisobga biriktirilgan."},
                status=status.HTTP_409_CONFLICT,
            )
        device, created = Device.objects.update_or_create(
            registration_id=reg_id,
            user=request.user,
            defaults={
                "platform": data.get("platform", Device.Platform.ANDROID),
                "active": data.get("active", True),
            },
        )
        out = self.get_serializer(device)
        code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(out.data, status=code)
