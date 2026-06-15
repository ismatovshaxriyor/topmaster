"""Chat API: conversations + messages."""
from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Conversation, ConversationParticipant, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    OpenConversationSerializer,
    SendMessageSerializer,
)
from .services import broadcast

User = get_user_model()


@extend_schema(tags=["Chat"])
class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    """List/retrieve the request user's conversations + open/messages/send actions."""

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.all()

    def get_queryset(self):
        user = self.request.user
        return (
            Conversation.objects.filter(memberships__user=user)
            .prefetch_related("memberships__user", "memberships__user__city")
            .select_related("last_message", "last_message__sender")
            .distinct()
        )

    def _other_participant(self, conversation):
        """Return the User on the other side of the conversation."""
        for membership in conversation.memberships.all():
            if membership.user_id != self.request.user.id:
                return membership.user
        return None

    @extend_schema(
        request=OpenConversationSerializer,
        responses=ConversationSerializer,
        summary="Open or create a 1:1 conversation",
    )
    @action(detail=False, methods=["post"])
    def open(self, request):
        ser = OpenConversationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        other_id = ser.validated_data["user"]
        job_id = ser.validated_data.get("job")

        if other_id == request.user.id:
            raise ValidationError("Oʻzingiz bilan suhbat ochib boʻlmaydi.")
        try:
            other = User.objects.get(pk=other_id)
        except User.DoesNotExist:
            raise ValidationError("Foydalanuvchi topilmadi.") from None

        # Find an existing 2-party conversation containing exactly the two
        # users (and matching job, if given).
        candidates = (
            Conversation.objects.filter(memberships__user=request.user)
            .filter(memberships__user=other)
            .filter(job_id=job_id)
            .distinct()
        )
        conversation = None
        for cand in candidates:
            if cand.memberships.count() == 2:
                conversation = cand
                break

        if conversation is None:
            conversation = Conversation.objects.create(job_id=job_id)
            ConversationParticipant.objects.bulk_create(
                [
                    ConversationParticipant(conversation=conversation, user=request.user),
                    ConversationParticipant(conversation=conversation, user=other),
                ]
            )

        conversation = self.get_queryset().get(pk=conversation.pk)
        data = ConversationSerializer(conversation, context=self.get_serializer_context()).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        responses=MessageSerializer(many=True),
        summary="List messages (oldest first); marks inbound as read",
    )
    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        qs = (
            conversation.messages.select_related("sender")
            .all()
            .order_by("created_at")
        )

        # Mark unread inbound messages as read for the request user.
        now = timezone.now()
        conversation.messages.filter(read_at__isnull=True).exclude(
            sender=request.user
        ).update(read_at=now)
        ConversationParticipant.objects.filter(
            conversation=conversation, user=request.user
        ).update(unread_count=0, last_read_at=now)

        broadcast(
            conversation.id,
            "chat.read",
            {"event": "read", "conversation_id": conversation.id, "user_id": request.user.id},
        )

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = MessageSerializer(page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(ser.data)
        ser = MessageSerializer(qs, many=True, context=self.get_serializer_context())
        return Response(ser.data)

    @extend_schema(
        request=SendMessageSerializer,
        responses=MessageSerializer,
        summary="Send a text message",
    )
    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        conversation = self.get_object()
        ser = SendMessageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        text = ser.validated_data["text"]

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=text,
            type=Message.Type.TEXT,
        )

        conversation.last_message = message
        conversation.save(update_fields=["last_message", "updated_at"])

        other = self._other_participant(conversation)
        if other is not None:
            ConversationParticipant.objects.filter(
                conversation=conversation, user=other
            ).update(unread_count=F("unread_count") + 1)

        data = MessageSerializer(message, context=self.get_serializer_context()).data
        broadcast(
            conversation.id,
            "chat.message",
            {"event": "message", "conversation_id": conversation.id, "message": data},
        )

        if other is not None:
            # Lazy import keeps the chat -> notifications direction acyclic.
            from apps.notifications.services import notify

            notify(
                other,
                type="chat",
                title=request.user.full_name or "Yangi xabar",
                body=text[:120],
                data={"conversation_id": conversation.id},
            )

        return Response(data, status=status.HTTP_201_CREATED)
