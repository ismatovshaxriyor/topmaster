"""Admin registration for catalog reference data."""
from django.contrib import admin

from apps.common.admin import MapPickerAdminMixin

from .models import Category, City


@admin.register(City)
class CityAdmin(MapPickerAdminMixin, admin.ModelAdmin):
    list_display = ("name", "slug", "order", "latitude", "longitude")
    list_editable = ("order",)
    list_filter = (("latitude", admin.EmptyFieldListFilter),)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "key")
    prepopulated_fields = {"key": ("label",)}
    ordering = ("order", "label")
