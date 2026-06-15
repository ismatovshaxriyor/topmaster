"""WebSocket consumer for live chat over a single conversation."""
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db import close_old_connections
from django.db.models import F
from django.utils import timezone

from .models import Conversation, ConversationParticipant, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """One socket per (user, conversation). Group: chat_<conversation_id>."""

    async def connect(self):
        self.conversation_id = int(self.scope["url_route"]["kwargs"]["conversation_id"])
        self.user = self.scope.get("user")

        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        if not await self._is_participant():
            await self.close()
            return

        self.group = f"chat_{self.conversation_id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        group = getattr(self, "group", None)
        if group:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        action = content.get("action")
        if action == "message":
            await self._handle_message(content.get("text", ""))
        elif action == "typing":
            await self.channel_layer.group_send(
                self.group,
                {
                    "type": "chat.typing",
                    "payload": {
                        "event": "typing",
                        "conversation_id": self.conversation_id,
                        "user_id": self.user.id,
                    },
                },
            )
        elif action == "read":
            await self._handle_read()

    async def _handle_message(self, text):
        text = (text or "").strip()
        if not text:
            return
        message = await self._persist_message(text)
        data = await self._serialize_message(message)
        await self.channel_layer.group_send(
            self.group,
            {
                "type": "chat.message",
                "payload": {
                    "event": "message",
                    "conversation_id": self.conversation_id,
                    "message": data,
                },
            },
        )
        await self._bump_and_notify(text)

    async def _handle_read(self):
        await self._mark_read()
        await self.channel_layer.group_send(
            self.group,
            {
                "type": "chat.read",
                "payload": {
                    "event": "read",
                    "conversation_id": self.conversation_id,
                    "user_id": self.user.id,
                },
            },
        )

    # ---- group event handlers ----
    async def chat_message(self, event):
        await self.send_json(event["payload"])

    async def chat_typing(self, event):
        await self.send_json(event["payload"])

    async def chat_read(self, event):
        await self.send_json(event["payload"])

    # ---- ORM helpers ----
    @database_sync_to_async
    def _is_participant(self):
        close_old_connections()
        return ConversationParticipant.objects.filter(
            conversation_id=self.conversation_id, user=self.user
        ).exists()

    @database_sync_to_async
    def _persist_message(self, text):
        close_old_connections()
        message = Message.objects.create(
            conversation_id=self.conversation_id,
            sender=self.user,
            text=text,
            type=Message.Type.TEXT,
        )
        Conversation.objects.filter(pk=self.conversation_id).update(
            last_message=message, updated_at=timezone.now()
        )
        return message

    @database_sync_to_async
    def _serialize_message(self, message):
        # Omit the request key entirely so FileField.use_url falls back to the
        # storage URL instead of calling None.build_absolute_uri().
        return MessageSerializer(message, context={}).data

    @database_sync_to_async
    def _mark_read(self):
        close_old_connections()
        now = timezone.now()
        Message.objects.filter(
            conversation_id=self.conversation_id, read_at__isnull=True
        ).exclude(sender=self.user).update(read_at=now)
        ConversationParticipant.objects.filter(
            conversation_id=self.conversation_id, user=self.user
        ).update(unread_count=0, last_read_at=now)

    @database_sync_to_async
    def _other_user(self):
        membership = (
            ConversationParticipant.objects.filter(conversation_id=self.conversation_id)
            .exclude(user=self.user)
            .select_related("user")
            .first()
        )
        return membership.user if membership else None

    @database_sync_to_async
    def _bump_unread(self):
        ConversationParticipant.objects.filter(
            conversation_id=self.conversation_id
        ).exclude(user=self.user).update(unread_count=F("unread_count") + 1)

    async def _bump_and_notify(self, text):
        await self._bump_unread()
        other = await self._other_user()
        if other is not None:
            await self._notify(other, text)

    @database_sync_to_async
    def _notify(self, other, text):
        # Lazy import keeps the chat -> notifications direction acyclic.
        from apps.notifications.services import notify

        notify(
            other,
            type="chat",
            title=self.user.full_name or "Yangi xabar",
            body=text[:120],
            data={"conversation_id": self.conversation_id},
        )
