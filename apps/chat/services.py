"""Shared chat helpers used by both the DRF views and the WS consumer."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def group_name(conversation_id) -> str:
    return f"chat_{conversation_id}"


def broadcast(conversation_id, message_type, payload):
    """Send an event to a conversation's channel group (sync context)."""
    layer = get_channel_layer()
    if layer is None:
        return
    async_to_sync(layer.group_send)(
        group_name(conversation_id),
        {"type": message_type, "payload": payload},
    )
