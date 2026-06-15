"""Accounts routes, mounted at /api/v1/auth/."""
from django.urls import include, path
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    DeviceViewSet,
    LoginView,
    LogoutView,
    MeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    SettingsView,
)

# SimpleJWT's view is used as-is; tag it so it lands under "Auth & Accounts"
# instead of a path-derived "v1" tag.
AuthTokenRefreshView = extend_schema_view(
    post=extend_schema(tags=["Auth & Accounts"])
)(TokenRefreshView)

router = DefaultRouter()
router.register("devices", DeviceViewSet, basename="device")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("token/refresh/", AuthTokenRefreshView.as_view(), name="auth-token-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me"),
    path("settings/", SettingsView.as_view(), name="auth-settings"),
    path("password/change/", ChangePasswordView.as_view(), name="auth-password-change"),
    path("password/reset/", PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="auth-password-reset-confirm",
    ),
    path("", include(router.urls)),
]
