"""Admin registration for notifications."""
from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "type", "title", "read", "created_at")
    list_filter = ("type", "read", "created_at")
    search_fields = ("title", "body", "recipient__email", "recipient__full_name")
    raw_id_fields = ("recipient",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
