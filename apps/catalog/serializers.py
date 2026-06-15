"""Serializers for catalog reference data (cities, categories)."""
from rest_framework import serializers

from .models import Category, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        # latitude/longitude let clients place cities on a map and power the
        # "nearby" feature client-side. Null for cities without seeded coords.
        fields = ("id", "name", "slug", "latitude", "longitude")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "key", "label", "icon")
