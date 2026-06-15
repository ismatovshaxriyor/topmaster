"""Filtering for the job board."""
import django_filters as filters

from .models import Job


class JobFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__key")
    city = filters.NumberFilter(field_name="city_id")
    price_type = filters.CharFilter(field_name="price_type")
    status = filters.CharFilter(field_name="status")
    urgent = filters.BooleanFilter(field_name="urgent")

    class Meta:
        model = Job
        fields = ("category", "city", "price_type", "status", "urgent")
