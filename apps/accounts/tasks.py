"""Background tasks for the accounts app."""
import logging
import secrets

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.cache import cache

from apps.common.email import send_html_email

logger = logging.getLogger(__name__)

# Codes live in the cache (Redis in prod) and expire on their own.
EMAIL_VERIFY_CACHE_KEY = "email_verify:{}"
PWD_RESET_CACHE_KEY = "pwd_reset:{}"
CODE_TTL = 15 * 60  # seconds
EMAIL_VERIFY_TTL = CODE_TTL  # backwards-compatible alias


def issue_email_verification_code(user_id) -> str:
    """Generate a fresh 6-digit code, store it (with TTL), and return it."""
    code = f"{secrets.randbelow(1_000_000):06d}"
    cache.set(EMAIL_VERIFY_CACHE_KEY.format(user_id), code, timeout=EMAIL_VERIFY_TTL)
    return code


@shared_task
def send_email_verification_code(user_id):
    """Email a fresh verification code to the user (best-effort, retryable)."""
    User = get_user_model()
    user = User.objects.filter(id=user_id, is_active=True).first()
    if user is None or user.email_verified:
        return
    code = issue_email_verification_code(user_id)
    send_html_email(
        "TopMaster: email tasdiqlash kodi",
        user.email,
        "verification_code",
        {"code": code, "name": user.full_name},
    )


def issue_password_reset_code(user_id) -> str:
    """Generate a fresh 6-digit password-reset code, cache it (TTL), and return it."""
    code = f"{secrets.randbelow(1_000_000):06d}"
    cache.set(PWD_RESET_CACHE_KEY.format(user_id), code, timeout=CODE_TTL)
    return code


@shared_task
def send_password_reset_code(user_id):
    """Email a fresh password-reset code to the user (best-effort, retryable)."""
    User = get_user_model()
    user = User.objects.filter(id=user_id, is_active=True).first()
    if user is None:
        return
    code = issue_password_reset_code(user_id)
    send_html_email(
        "TopMaster: parolni tiklash kodi",
        user.email,
        "password_reset",
        {"code": code, "name": user.full_name},
    )
