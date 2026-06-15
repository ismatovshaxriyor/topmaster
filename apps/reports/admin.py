"""Admin moderation for abuse reports — open reports float to the top."""
from django.contrib import admin
from django.db.models import Case, IntegerField, Value, When
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Report

_STATUS_COLORS = {
    Report.Status.OPEN: "#dc2626",       # red — needs attention
    Report.Status.REVIEWING: "#d97706",  # amber
    Report.Status.RESOLVED: "#16a34a",   # green
    Report.Status.DISMISSED: "#6b7280",  # grey
}


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "target_link",
        "reason",
        "status_badge",
        "reporter",
        "created_at",
        "handled_by",
    )
    list_filter = ("status", "reason", "content_type")
    search_fields = (
        "description",
        "resolution_note",
        "reporter__email",
        "reporter__full_name",
    )
    readonly_fields = (
        "target_link",
        "reporter",
        "reason",
        "description",
        "content_type",
        "object_id",
        "handled_by",
        "resolved_at",
        "created_at",
        "updated_at",
    )
    fields = (
        "target_link",
        "reporter",
        "reason",
        "description",
        "status",
        "resolution_note",
        "handled_by",
        "resolved_at",
        "created_at",
    )
    actions = ("mark_reviewing", "mark_resolved", "mark_dismissed")

    # New (open) reports sort above in-progress, then resolved, then dismissed.
    _STATUS_PRIORITY = Case(
        When(status=Report.Status.OPEN, then=Value(0)),
        When(status=Report.Status.REVIEWING, then=Value(1)),
        When(status=Report.Status.RESOLVED, then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )

    def get_queryset(self, request):
        return (
            self.model._default_manager.get_queryset()
            .select_related("content_type", "reporter", "handled_by")
            .annotate(_priority=self._STATUS_PRIORITY)
            .order_by("_priority", "-created_at")
        )

    @admin.display(description="Obyekt")
    def target_link(self, obj):
        target = obj.target
        label = (
            str(target)
            if target is not None
            else f"{obj.content_type.model} #{obj.object_id}"
        )
        try:
            url = reverse(
                f"admin:{obj.content_type.app_label}_{obj.content_type.model}_change",
                args=[obj.object_id],
            )
            return format_html('<a href="{}">{}</a>', url, label)
        except Exception:
            return label

    @admin.display(description="Holat")
    def status_badge(self, obj):
        color = _STATUS_COLORS.get(obj.status, "#6b7280")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:10px;font-size:11px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    def save_model(self, request, obj, form, change):
        # Stamp the moderator + resolution time when the status is changed here.
        if "status" in getattr(form, "changed_data", []):
            obj.handled_by = request.user
            if obj.status in (Report.Status.RESOLVED, Report.Status.DISMISSED):
                obj.resolved_at = obj.resolved_at or timezone.now()
        super().save_model(request, obj, form, change)

    @admin.action(description="Ko'rib chiqilmoqda deb belgilash")
    def mark_reviewing(self, request, queryset):
        n = queryset.update(status=Report.Status.REVIEWING, handled_by=request.user)
        self.message_user(request, f"{n} ta shikoyat ko'rib chiqilmoqda.")

    @admin.action(description="Hal qilindi deb belgilash")
    def mark_resolved(self, request, queryset):
        n = queryset.update(
            status=Report.Status.RESOLVED,
            handled_by=request.user,
            resolved_at=timezone.now(),
        )
        self.message_user(request, f"{n} ta shikoyat hal qilindi.")

    @admin.action(description="Rad etish")
    def mark_dismissed(self, request, queryset):
        n = queryset.update(
            status=Report.Status.DISMISSED,
            handled_by=request.user,
            resolved_at=timezone.now(),
        )
        self.message_user(request, f"{n} ta shikoyat rad etildi.")
