"""Admin registration for proposals."""
from django.contrib import admin

from .models import Proposal


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "master", "status", "proposed_price", "created_at")
    list_filter = ("status",)
    search_fields = ("job__title", "master__user__email", "message")
    raw_id_fields = ("job", "master")
    readonly_fields = ("created_at", "updated_at", "responded_at")
    list_select_related = ("job", "master", "master__user")
