"""Admin registration for favorites."""
from django.contrib import admin

from .models import SavedMaster


@admin.register(SavedMaster)
class SavedMasterAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "master", "created_at")
    list_select_related = ("client", "master", "master__user")
    search_fields = ("client__email", "master__user__email", "master__user__full_name")
    raw_id_fields = ("client", "master")
    ordering = ("-created_at",)
