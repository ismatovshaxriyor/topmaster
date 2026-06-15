"""Celery tasks for push delivery via Firebase Cloud Messaging."""
import logging

from celery import shared_task
from django.conf import settings

from .models import Notification

logger = logging.getLogger(__name__)

# Module-level flag to guard against double firebase_admin initialisation.
_firebase_initialized = False


def _ensure_firebase():
    """Lazily initialise the firebase_admin SDK exactly once."""
    global _firebase_initialized
    import firebase_admin
    from firebase_admin import credentials

    if _firebase_initialized or firebase_admin._apps:
        _firebase_initialized = True
        return
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)
    firebase_admin.initialize_app(cred)
    _firebase_initialized = True


@shared_task
def send_fcm_push(notification_id):
    """Send an FCM multicast push for a notification to the recipient's devices."""
    try:
        notification = Notification.objects.select_related("recipient").get(pk=notification_id)
    except Notification.DoesNotExist:
        logger.warning("send_fcm_push: notification %s not found", notification_id)
        return

    registration_ids = list(
        notification.recipient.devices.filter(active=True).values_list(
            "registration_id", flat=True
        )
    )
    if not registration_ids:
        return

    if not settings.FIREBASE_CREDENTIALS_FILE:
        logger.info("FCM disabled (FIREBASE_CREDENTIALS_FILE unset); skipping push.")
        return

    try:
        _ensure_firebase()
        from firebase_admin import messaging

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.body or "",
            ),
            data={k: str(v) for k, v in (notification.data or {}).items()},
            tokens=registration_ids,
        )
        messaging.send_each_for_multicast(message)
    except Exception:  # pragma: no cover - external service
        logger.exception("Failed to send FCM push for notification %s", notification_id)
