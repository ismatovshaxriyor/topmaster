"""WebSocket consumer for live notification delivery."""
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """Per-user notification stream.

    Joins group ``user_<id>``. The server pushes new notifications and
    unread-count updates; the client is not expected to send anything.
    """

    async def connect(self):
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        unread = await self._unread_count(user)
        await self.send_json({"event": "unread", "unread": unread})

    async def disconnect(self, code):
        group_name = getattr(self, "group_name", None)
        if group_name:
            await self.channel_layer.group_discard(group_name, self.channel_name)

    # ── group_send handlers ───────────────────────────────────────
    async def notify_message(self, event):
        await self.send_json(event["payload"])

    async def notify_unread(self, event):
        await self.send_json(event["payload"])

    # ── helpers ────────────────────────────────────────────────────
    @database_sync_to_async
    def _unread_count(self, user):
        return user.notifications.filter(read=False).count()
