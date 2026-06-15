"""Filters for the public masters list."""
import django_filters as filters

from .models import AvailabilityStatus, MasterProfile


class MasterFilter(filters.FilterSet):
    city = filters.NumberFilter(field_name="user__city_id")
    category = filters.CharFilter(field_name="categories__key", distinct=True)
    status = filters.ChoiceFilter(choices=AvailabilityStatus.choices)
    verified = filters.BooleanFilter(field_name="is_verified")
    top = filters.BooleanFilter(field_name="is_top")
    rating_min = filters.NumberFilter(field_name="rating_avg", lookup_expr="gte")

    class Meta:
        model = MasterProfile
        fields = ("city", "category", "status", "verified", "top", "rating_min")
