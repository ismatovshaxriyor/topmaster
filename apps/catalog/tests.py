"""Catalog endpoint tests: public city/category lists return seeded data."""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.catalog.models import Category, City


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def seed_catalog(db):
    City.objects.create(
        name="Toshkent", slug="toshkent", order=0,
        latitude=41.2995, longitude=69.2401,
    )
    City.objects.create(name="Samarqand", slug="samarqand", order=1)
    Category.objects.create(key="elektrik", label="Elektrik", icon="zap", order=0)
    Category.objects.create(
        key="santexnik", label="Santexnik", icon="wrench", order=1
    )
    # Inactive categories must be hidden from the list endpoint.
    Category.objects.create(
        key="arxiv", label="Arxiv", icon="wrench", order=2, is_active=False
    )


def test_cities_list_public(api_client, seed_catalog):
    resp = api_client.get(reverse("catalog-city-list"))
    assert resp.status_code == 200
    # Paginated response: {count, next, previous, results}.
    assert resp.data["count"] == 2
    results = resp.data["results"]
    names = [c["name"] for c in results]
    assert names == ["Toshkent", "Samarqand"]
    assert set(results[0].keys()) == {"id", "name", "slug", "latitude", "longitude"}
    # Coordinates pass through; cities without coords return null.
    assert results[0]["latitude"] == 41.2995
    assert results[0]["longitude"] == 69.2401
    assert results[1]["latitude"] is None


def test_categories_list_excludes_inactive(api_client, seed_catalog):
    resp = api_client.get(reverse("catalog-category-list"))
    assert resp.status_code == 200
    results = resp.data["results"]
    keys = [c["key"] for c in results]
    assert keys == ["elektrik", "santexnik"]
    assert "arxiv" not in keys
    assert set(results[0].keys()) == {"id", "key", "label", "icon"}
