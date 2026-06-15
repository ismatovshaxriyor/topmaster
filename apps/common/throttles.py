"""Custom DRF throttles for abuse-sensitive endpoints.

Each class's ``scope`` maps to a rate in
``settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']``. The anonymous-scoped
throttles key on client IP (brute-force / enumeration protection on auth
endpoints); the support one keys on the authenticated user.
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """Limit login attempts per IP — slows credential-stuffing."""

    scope = "login"


class RegisterRateThrottle(AnonRateThrottle):
    """Limit account creation per IP — slows bulk sign-up abuse."""

    scope = "register"


class PasswordResetRateThrottle(AnonRateThrottle):
    """Limit reset requests/confirms per IP — slows enumeration + spam."""

    scope = "password_reset"


class SupportSendRateThrottle(UserRateThrottle):
    """Limit support-chat messages per user — slows flooding."""

    scope = "support_send"


class ReportRateThrottle(UserRateThrottle):
    """Limit abuse reports per user — slows report-spam / brigading."""

    scope = "report"
