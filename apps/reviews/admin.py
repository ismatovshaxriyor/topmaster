"""Admin registration for reviews."""
from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "master", "author", "rating", "recommend", "created_at")
    list_filter = ("rating", "recommend", "created_at")
    search_fields = ("master__user__full_name", "author__full_name", "author__email", "text")
    autocomplete_fields = ("job", "author", "master")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
