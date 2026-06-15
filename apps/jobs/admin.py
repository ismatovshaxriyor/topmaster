"""Admin registration for the jobs app."""
from django.contrib import admin

from apps.common.admin import MapPickerAdminMixin

from .models import Job, JobEvent, JobImage


class JobImageInline(admin.TabularInline):
    model = JobImage
    extra = 0


class JobEventInline(admin.TabularInline):
    model = JobEvent
    extra = 0
    readonly_fields = ("type", "actor", "note", "created_at")
    can_delete = False


@admin.register(Job)
class JobAdmin(MapPickerAdminMixin, admin.ModelAdmin):
    list_display = ("id", "title", "client", "category", "city", "status", "urgent", "proposals_count", "created_at")
    list_filter = ("status", "price_type", "urgent", "when_choice")
    search_fields = ("title", "description", "client__email", "client__full_name")
    raw_id_fields = ("client", "category", "city", "assigned_master")
    inlines = (JobImageInline, JobEventInline)
    date_hierarchy = "created_at"
