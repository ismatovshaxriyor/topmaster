"""Background tasks for the accounts app."""
import logging
import secrets

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

# The verification code lives in the cache (Redis in prod) and expires on its own.
EMAIL_VERIFY_CACHE_KEY = "email_verify:{}"
EMAIL_VERIFY_TTL = 15 * 60  # seconds


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
    send_mail(
        subject="TopMaster: email tasdiqlash kodi",
        message=(
            "Assalomu alaykum!\n\n"
            f"Email manzilingizni tasdiqlash kodi: {code}\n\n"
            "Kod 15 daqiqa amal qiladi. Agar siz roʻyxatdan oʻtmagan boʻlsangiz, "
            "ushbu xabarni eʼtiborsiz qoldiring."
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )
