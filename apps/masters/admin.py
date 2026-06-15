"""Admin registrations for the masters app."""
from django.contrib import admin
from django.utils import timezone

from apps.common.admin import MapPickerAdminMixin

from .models import (
    MasterProfile,
    PortfolioItem,
    Skill,
    VerificationDocument,
    VerificationRequest,
)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem
    extra = 0


@admin.register(MasterProfile)
class MasterProfileAdmin(MapPickerAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "is_verified",
        "is_top",
        "rating_avg",
        "reviews_count",
        "views_count",
    )
    list_filter = ("status", "is_verified", "is_top")
    search_fields = ("user__full_name", "user__email")
    autocomplete_fields = ("user", "categories")
    inlines = (SkillInline, PortfolioItemInline)


class VerificationDocumentInline(admin.TabularInline):
    model = VerificationDocument
    extra = 0


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "master", "status", "submitted_at", "reviewed_at")
    list_filter = ("status",)
    search_fields = ("master__user__full_name", "master__user__email")
    inlines = (VerificationDocumentInline,)
    actions = ("approve_verification",)

    @admin.action(description="Tasdiqlangan deb belgilash")
    def approve_verification(self, request, queryset):
        now = timezone.now()
        for vreq in queryset:
            vreq.status = VerificationRequest.Status.APPROVED
            vreq.reviewed_at = now
            vreq.reviewer = request.user
            vreq.save(update_fields=["status", "reviewed_at", "reviewer", "updated_at"])
            master = vreq.master
            master.is_verified = True
            master.save(update_fields=["is_verified", "updated_at"])
        self.message_user(request, f"{queryset.count()} ta so'rov tasdiqlandi.")
