"""Lightweight API tests for the notifications app."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.notifications.models import Notification

User = get_user_model()


@pytest.fixture
def users(db):
    a = User.objects.create_user(email="a@example.com", password="pass12345")
    b = User.objects.create_user(email="b@example.com", password="pass12345")
    return a, b


@pytest.fixture
def client_for():
    def _make(user):
        c = APIClient()
        c.force_authenticate(user=user)
        return c

    return _make


def test_list_is_scoped_to_user(users, client_for):
    a, b = users
    Notification.objects.create(recipient=a, type="system", title="A1")
    Notification.objects.create(recipient=a, type="order", title="A2")
    Notification.objects.create(recipient=b, type="system", title="B1")

    resp = client_for(a).get("/api/v1/notifications/")
    assert resp.status_code == 200
    titles = {n["title"] for n in resp.data["results"]}
    assert titles == {"A1", "A2"}


def test_unread_count(users, client_for):
    a, _ = users
    Notification.objects.create(recipient=a, type="system", title="x")
    Notification.objects.create(recipient=a, type="system", title="y", read=True)

    resp = client_for(a).get("/api/v1/notifications/unread_count/")
    assert resp.status_code == 200
    assert resp.data["unread"] == 1


def test_mark_read_flips_flag(users, client_for):
    a, _ = users
    n = Notification.objects.create(recipient=a, type="system", title="x")

    resp = client_for(a).post(f"/api/v1/notifications/{n.id}/mark_read/")
    assert resp.status_code == 200
    assert resp.data["read"] is True
    n.refresh_from_db()
    assert n.read is True


def test_mark_all_read(users, client_for):
    a, _ = users
    Notification.objects.create(recipient=a, type="system", title="x")
    Notification.objects.create(recipient=a, type="system", title="y")

    resp = client_for(a).post("/api/v1/notifications/mark_all_read/")
    assert resp.status_code == 200
    assert resp.data["updated"] == 2
    assert a.notifications.filter(read=False).count() == 0


def test_cannot_mark_other_users_notification(users, client_for):
    a, b = users
    n = Notification.objects.create(recipient=b, type="system", title="B")

    resp = client_for(a).post(f"/api/v1/notifications/{n.id}/mark_read/")
    assert resp.status_code == 404


def test_requires_authentication():
    resp = APIClient().get("/api/v1/notifications/")
    assert resp.status_code in (401, 403)
