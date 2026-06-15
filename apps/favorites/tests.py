"""Tests for the favorites app: add, list, idempotent duplicate, remove."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.favorites.models import SavedMaster
from apps.masters.models import MasterProfile

User = get_user_model()


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        email="client@example.com", password="pass12345", full_name="Mijoz Bir"
    )


@pytest.fixture
def master(db):
    usta = User.objects.create_user(
        email="usta@example.com", password="pass12345", full_name="Usta Bir", role="usta"
    )
    return MasterProfile.objects.create(user=usta)


@pytest.fixture
def api(client_user):
    c = APIClient()
    c.force_authenticate(user=client_user)
    return c


def test_add_master(api, master):
    resp = api.post("/api/v1/favorites/", {"master": master.id})
    assert resp.status_code == 201
    assert SavedMaster.objects.filter(master=master).count() == 1


def test_duplicate_is_idempotent(api, master):
    first = api.post("/api/v1/favorites/", {"master": master.id})
    second = api.post("/api/v1/favorites/", {"master": master.id})
    assert first.status_code == 201
    assert second.status_code == 200
    assert SavedMaster.objects.filter(master=master).count() == 1


def test_list_and_ids(api, master, client_user):
    SavedMaster.objects.create(client=client_user, master=master)
    listing = api.get("/api/v1/favorites/")
    assert listing.status_code == 200
    results = listing.data.get("results", listing.data)
    assert len(results) == 1
    assert results[0]["master"]["id"] == master.id

    ids = api.get("/api/v1/favorites/ids/")
    assert ids.status_code == 200
    assert ids.data["ids"] == [master.id]


def test_remove(api, master, client_user):
    saved = SavedMaster.objects.create(client=client_user, master=master)
    resp = api.delete(f"/api/v1/favorites/{saved.id}/")
    assert resp.status_code == 204
    assert not SavedMaster.objects.filter(id=saved.id).exists()


def test_requires_auth(master):
    anon = APIClient()
    resp = anon.get("/api/v1/favorites/")
    assert resp.status_code in (401, 403)
