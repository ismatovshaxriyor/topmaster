"""Admin for chat conversations and messages."""
from django.contrib import admin

from .models import Conversation, ConversationParticipant, Message


class ConversationParticipantInline(admin.TabularInline):
    model = ConversationParticipant
    extra = 0
    raw_id_fields = ("user",)
    readonly_fields = ("unread_count", "last_read_at")


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ("sender", "type", "text", "read_at", "created_at")
    readonly_fields = ("sender", "type", "text", "read_at", "created_at")
    raw_id_fields = ("sender",)
    show_change_link = True
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "last_message", "updated_at", "created_at")
    list_filter = ("created_at",)
    search_fields = ("id", "memberships__user__email")
    raw_id_fields = ("job", "last_message")
    inlines = (ConversationParticipantInline, MessageInline)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "type", "short_text", "read_at", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("text", "sender__email")
    raw_id_fields = ("conversation", "sender")

    @admin.display(description="text")
    def short_text(self, obj):
        return (obj.text or "")[:60]
