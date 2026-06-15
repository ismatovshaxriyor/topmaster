"""Admin registrations for accounts models."""
from django.contrib import admin

from .models import Device, User, UserSettings


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "role", "city", "is_verified", "is_active", "is_staff")
    list_filter = ("role", "is_verified", "is_active", "is_staff")
    search_fields = ("email", "full_name", "phone")
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login")


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "language", "theme", "notif_push", "notif_email", "twofa")
    list_filter = ("language", "theme", "notif_push")
    search_fields = ("user__email", "user__full_name")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "platform", "active", "created_at")
    list_filter = ("platform", "active")
    search_fields = ("user__email", "registration_id")
