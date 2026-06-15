"""Lightweight API tests for the masters app."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.masters.models import MasterProfile

User = get_user_model()


@pytest.fixture
def client_api():
    return APIClient()


@pytest.fixture
def master_user(db):
    user = User.objects.create_user(
        email="usta@example.com", password="pass12345", role="usta", full_name="Ali Usta"
    )
    return user


@pytest.fixture
def master_profile(master_user):
    return MasterProfile.objects.create(user=master_user, experience_years=5, min_price=100000)


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        email="mijoz@example.com", password="pass12345", role="mijoz", full_name="Vali Mijoz"
    )


def test_master_list_public(client_api, master_profile):
    resp = client_api.get("/api/v1/masters/")
    assert resp.status_code == 200
    results = resp.data.get("results", resp.data)
    assert any(m["id"] == master_profile.id for m in results)


def test_master_detail_public_and_increments_views(client_api, master_profile):
    assert master_profile.views_count == 0
    resp = client_api.get(f"/api/v1/masters/{master_profile.id}/")
    assert resp.status_code == 200
    assert resp.data["views_count"] == 1
    master_profile.refresh_from_db()
    assert master_profile.views_count == 1


def test_me_update_requires_master_role(client_api, client_user):
    client_api.force_authenticate(client_user)
    resp = client_api.patch("/api/v1/masters/me/", {"bio": "salom"}, format="json")
    assert resp.status_code == 403


def test_master_can_update_own_profile(client_api, master_user, master_profile):
    client_api.force_authenticate(master_user)
    resp = client_api.patch(
        "/api/v1/masters/me/", {"bio": "Tajribali elektrik", "min_price": 200000}, format="json"
    )
    assert resp.status_code == 200
    master_profile.refresh_from_db()
    assert master_profile.bio == "Tajribali elektrik"
    assert master_profile.min_price == 200000


def test_master_fulltext_search_by_name_and_bio(db, client_api):
    u1 = User.objects.create_user(
        email="a@e.uz", password="p", role="usta", full_name="Aziz Elektrik"
    )
    m1 = MasterProfile.objects.create(user=u1, bio="Tajribali elektrik, simlarni ulayman")
    u2 = User.objects.create_user(
        email="b@e.uz", password="p", role="usta", full_name="Bobur Santexnik"
    )
    m2 = MasterProfile.objects.create(user=u2, bio="Quvurlarni taʼmirlayman")
    resp = client_api.get("/api/v1/masters/", {"q": "elektrik"})
    assert resp.status_code == 200, resp.content
    ids = [m["id"] for m in resp.data["results"]]
    assert m1.id in ids
    assert m2.id not in ids


def test_master_search_matches_skill_title(db, client_api):
    from apps.masters.models import Skill

    u1 = User.objects.create_user(
        email="c@e.uz", password="p", role="usta", full_name="Karim Aka"
    )
    m1 = MasterProfile.objects.create(user=u1, bio="umumiy ishlar")
    Skill.objects.create(master=m1, title="Konditsioner tozalash", price_min=50000)
    u2 = User.objects.create_user(
        email="d@e.uz", password="p", role="usta", full_name="Olim Aka"
    )
    m2 = MasterProfile.objects.create(user=u2, bio="boshqa ish")
    resp = client_api.get("/api/v1/masters/", {"q": "konditsioner"})
    assert resp.status_code == 200, resp.content
    ids = [m["id"] for m in resp.data["results"]]
    assert m1.id in ids  # matched via skill title, not name/bio
    assert m2.id not in ids


def test_master_nearby_search_orders_and_filters_by_distance(db, client_api):
    from apps.catalog.models import City

    tashkent = City.objects.create(
        name="T-test", slug="t-test", latitude=41.2995, longitude=69.2401
    )
    samarkand = City.objects.create(
        name="S-test", slug="s-test", latitude=39.6270, longitude=66.9750
    )
    u1 = User.objects.create_user(
        email="t@e.uz", password="p", role="usta", full_name="T Usta", city=tashkent
    )
    m1 = MasterProfile.objects.create(user=u1)
    u2 = User.objects.create_user(
        email="s@e.uz", password="p", role="usta", full_name="S Usta", city=samarkand
    )
    m2 = MasterProfile.objects.create(user=u2)

    # Search near Tashkent: closest master first, with a distance value.
    resp = client_api.get("/api/v1/masters/", {"lat": 41.3, "lng": 69.24})
    assert resp.status_code == 200, resp.content
    results = resp.data["results"]
    assert results[0]["id"] == m1.id
    assert results[0]["distance_km"] is not None
    assert results[0]["distance_km"] < results[1]["distance_km"]

    # radius_km caps the result set.
    resp2 = client_api.get(
        "/api/v1/masters/", {"lat": 41.3, "lng": 69.24, "radius_km": 50}
    )
    ids = [m["id"] for m in resp2.data["results"]]
    assert m1.id in ids
    assert m2.id not in ids


def test_create_skill(client_api, master_user, master_profile):
    client_api.force_authenticate(master_user)
    resp = client_api.post(
        "/api/v1/masters/me/skills/",
        {"title": "Rozetka oʻrnatish", "price_min": 50000, "years": 3},
        format="json",
    )
    assert resp.status_code == 201
    assert master_profile.skills.count() == 1
