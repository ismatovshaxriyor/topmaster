"""Chat serializers: messages and conversations."""
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.accounts.serializers import UserSummarySerializer

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """A single chat message."""

    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)
    attachment = serializers.FileField(use_url=True, read_only=True)
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "sender_name",
            "type",
            "text",
            "attachment",
            "created_at",
            "read_at",
            "is_mine",
        )
        read_only_fields = fields

    def get_is_mine(self, obj) -> bool:
        request = self.context.get("request")
        user = getattr(request, "user", None)
        return bool(user and obj.sender_id == user.id)


class ConversationSerializer(serializers.ModelSerializer):
    """A conversation rendered for one side (the request user)."""

    other = serializers.SerializerMethodField()
    last_message = MessageSerializer(read_only=True)
    unread = serializers.SerializerMethodField()
    job = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Conversation
        fields = ("id", "other", "last_message", "unread", "job", "updated_at")
        read_only_fields = fields

    def _current_user(self):
        request = self.context.get("request")
        return getattr(request, "user", None)

    @extend_schema_field(UserSummarySerializer)
    def get_other(self, obj):
        """The participant that is NOT the request user."""
        user = self._current_user()
        memberships = obj.memberships.all()
        for membership in memberships:
            if not user or membership.user_id != user.id:
                return UserSummarySerializer(
                    membership.user, context=self.context
                ).data
        return None

    def get_unread(self, obj) -> int:
        user = self._current_user()
        if not user:
            return 0
        for membership in obj.memberships.all():
            if membership.user_id == user.id:
                return membership.unread_count
        return 0


class OpenConversationSerializer(serializers.Serializer):
    """Input for opening/creating a 1:1 conversation."""

    user = serializers.IntegerField()
    job = serializers.IntegerField(required=False, allow_null=True)


class SendMessageSerializer(serializers.Serializer):
    """Input for posting a text message."""

    text = serializers.CharField(allow_blank=False, trim_whitespace=True)
