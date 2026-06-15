"""Support-chat side effects shared by the API and the admin reply flow."""
from django.utils import timezone


def register_staff_reply(message):
    """Apply a support-team reply to its thread and notify the user live.

    Sets the message as staff-authored, refreshes the thread's denormalised
    fields, and pushes a WebSocket + FCM + in-app notification to the user.
    Safe to call from the Django admin (sync) and the API.
    """
    thread = message.thread
    thread.last_message = message
    thread.user_unread = (thread.user_unread or 0) + 1
    thread.staff_unread = 0
    if thread.status in (thread.Status.OPEN, thread.Status.PENDING):
        thread.status = thread.Status.PENDING  # awaiting the user now
    thread.save(update_fields=["last_message", "user_unread", "staff_unread", "status", "updated_at"])

    # Lazy import keeps support -> notifications acyclic and admin-safe.
    try:
        from apps.notifications.services import notify

        notify(
            thread.user,
            type="system",
            title="Qo'llab-quvvatlash javob berdi",
            body=(message.text or "Yangi xabar")[:140],
            data={"support_thread_id": thread.id, "message_id": message.id},
        )
    except Exception:  # notifications must never break a support reply
        pass


def register_user_message(thread, message):
    """Apply a user's message to the thread.

    Any user message moves the thread to OPEN — the ball is now in the support
    team's court (awaiting a reply) — and bumps the staff-unread counter.
    """
    thread.last_message = message
    thread.staff_unread = (thread.staff_unread or 0) + 1
    if thread.status != thread.Status.OPEN:
        thread.status = thread.Status.OPEN
    thread.save(update_fields=["last_message", "staff_unread", "status", "updated_at"])


def mark_staff_messages_read(thread):
    """The user has read staff replies — clear their unread counter."""
    now = timezone.now()
    thread.messages.filter(is_staff=True, read_at__isnull=True).update(read_at=now)
    if thread.user_unread:
        thread.user_unread = 0
        thread.save(update_fields=["user_unread", "updated_at"])
