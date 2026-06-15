"""Shared admin building blocks.

* ``MapPickerAdminMixin`` — drops a Leaflet location picker onto any ModelAdmin
  whose model has ``latitude`` / ``longitude`` fields.
* A prettier, read-only admin for django-auditlog's ``LogEntry`` (colored action
  badges + a readable field/old/new change table), replacing the plain default.
"""
import contextlib

from django.contrib import admin
from django.utils.html import format_html, format_html_join


class MapPickerAdminMixin:
    """Render a click-to-set OpenStreetMap picker for latitude/longitude.

    The picker template auto-binds to ``#id_latitude`` / ``#id_longitude`` so no
    per-admin wiring is needed beyond mixing this in.
    """

    change_form_template = "admin/map_picker_change_form.html"


# ── Pretty audit log ──────────────────────────────────────────────
try:
    from auditlog.models import LogEntry
except Exception:  # auditlog optional — skip if unavailable
    LogEntry = None

_ACTION_COLORS = {0: "#16a34a", 1: "#d97706", 2: "#dc2626", 3: "#6b7280"}


def _fmt(value):
    if value is None or value == "None":
        return "∅"
    s = str(value)
    return (s[:80] + "…") if len(s) > 80 else s


def _changes(obj):
    """Return the {field: [old, new]} change map across auditlog versions."""
    data = getattr(obj, "changes_dict", None)
    if callable(data):
        try:
            data = data()
        except Exception:
            data = None
    return data if isinstance(data, dict) else {}


if LogEntry is not None:
    with contextlib.suppress(admin.sites.NotRegistered):
        admin.site.unregister(LogEntry)

    @admin.register(LogEntry)
    class PrettyLogEntryAdmin(admin.ModelAdmin):
        """Read-only, human-friendly view of the audit trail."""

        list_display = (
            "timestamp",
            "actor_label",
            "action_badge",
            "resource",
            "object_repr",
            "change_summary",
        )
        list_filter = ("action", "content_type", "timestamp")
        search_fields = ("object_repr", "actor__email", "actor__full_name", "changes")
        date_hierarchy = "timestamp"
        list_select_related = ("content_type", "actor")
        fields = (
            "timestamp",
            "actor_label",
            "action_badge",
            "resource",
            "object_repr",
            "remote_addr",
            "changes_table",
        )
        readonly_fields = fields

        # Audit entries are immutable — view only.
        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

        @admin.display(description="Kim", ordering="actor")
        def actor_label(self, obj):
            return obj.actor or "Tizim"

        @admin.display(description="Amal", ordering="action")
        def action_badge(self, obj):
            color = _ACTION_COLORS.get(obj.action, "#6b7280")
            return format_html(
                '<span style="background:{};color:#fff;padding:2px 8px;'
                'border-radius:10px;font-size:11px;">{}</span>',
                color,
                obj.get_action_display(),
            )

        @admin.display(description="Obyekt turi", ordering="content_type")
        def resource(self, obj):
            return obj.content_type

        @admin.display(description="O'zgargan maydonlar")
        def change_summary(self, obj):
            keys = list(_changes(obj).keys())
            if not keys:
                return "—"
            extra = f" +{len(keys) - 3}" if len(keys) > 3 else ""
            return ", ".join(keys[:3]) + extra

        @admin.display(description="O'zgarishlar")
        def changes_table(self, obj):
            data = _changes(obj)
            pairs = [
                (field, _fmt(vals[0]), _fmt(vals[1]))
                for field, vals in data.items()
                if isinstance(vals, list | tuple) and len(vals) == 2
            ]
            if not pairs:
                return "—"
            body = format_html_join(
                "",
                "<tr>"
                '<td style="padding:4px 12px;font-weight:600;border-top:1px solid #eee;">{}</td>'
                '<td style="padding:4px 12px;color:#b91c1c;border-top:1px solid #eee;">{}</td>'
                '<td style="padding:4px 12px;color:#15803d;border-top:1px solid #eee;">{}</td>'
                "</tr>",
                pairs,
            )
            return format_html(
                '<table style="border-collapse:collapse;font-size:13px;">'
                '<thead><tr>'
                '<th style="text-align:left;padding:4px 12px;">Maydon</th>'
                '<th style="text-align:left;padding:4px 12px;">Eski</th>'
                '<th style="text-align:left;padding:4px 12px;">Yangi</th>'
                "</tr></thead><tbody>{}</tbody></table>",
                body,
            )
