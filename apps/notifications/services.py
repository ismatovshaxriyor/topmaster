"""Notification delivery service.

`notify()` is the single cross-app entry point: it persists a Notification,
pushes it live over WebSocket, and enqueues an FCM push. Failures in the
real-time / push layers are logged but never raised — creating the record
must always succeed for the caller.
"""
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification
from .serializers import NotificationSerializer

logger = logging.getLogger(__name__)


def _group_name(user_id) -> str:
    return f"user_{user_id}"


def notify(recipient, *, type, title, body="", data=None, push=True):
    """Create a notification, broadcast it live, and enqueue a push.

    Returns the created Notification. Never raises on transport failure.
    """
    notification = Notification.objects.create(
        recipient=recipient,
        type=type,
        title=title,
        body=body,
        data=data or {},
    )

    payload_data = NotificationSerializer(notification).data
    unread = recipient.notifications.filter(read=False).count()

    # Live WebSocket delivery.
    try:
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            async_to_sync(channel_layer.group_send)(
                _group_name(recipient.id),
                {
                    "type": "notify.message",
                    "payload": {
                        "event": "notification",
                        "notification": payload_data,
                        "unread": unread,
                    },
                },
            )
    except Exception:  # pragma: no cover - transport failure must not break caller
        logger.exception("Failed to push notification %s over WebSocket", notification.id)

    # FCM push (respect per-user preference).
    if push and getattr(getattr(recipient, "settings", None), "notif_push", True):
        try:
            from .tasks import send_fcm_push

            send_fcm_push.delay(notification.id)
        except Exception:  # pragma: no cover
            logger.exception("Failed to enqueue FCM push for notification %s", notification.id)

    return notification


def send_unread_count(user):
    """Group-send the current unread count to a user's live socket(s)."""
    try:
        channel_layer = get_channel_layer()
        if channel_layer is None:
            return
        unread = user.notifications.filter(read=False).count()
        async_to_sync(channel_layer.group_send)(
            _group_name(user.id),
            {
                "type": "notify.message",
                "payload": {"event": "unread", "unread": unread},
            },
        )
    except Exception:  # pragma: no cover
        logger.exception("Failed to send unread count for user %s", getattr(user, "id", None))
