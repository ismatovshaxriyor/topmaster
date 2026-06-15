"""Tests for the reviews app."""
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.jobs.models import Job, JobStatus
from apps.masters.models import MasterProfile
from apps.reviews.models import Review

pytestmark = pytest.mark.django_db
User = get_user_model()

# notify() hits WebSockets/FCM — stub it for the whole module.
NOTIFY_PATH = "apps.notifications.services.notify"


def _make_master():
    user = User.objects.create_user(
        email="usta@example.com", password="pw12345", role="usta"
    )
    return MasterProfile.objects.create(user=user)


def _make_client(email="mijoz@example.com"):
    return User.objects.create_user(email=email, password="pw12345", role="mijoz")


def _completed_job(client, master):
    return Job.objects.create(
        client=client,
        title="Rozetka almashtirish",
        description="Kuhxonadagi rozetka ishlamayapti.",
        status=JobStatus.COMPLETED,
        assigned_master=master,
    )


def test_client_can_review_completed_assigned_job():
    master = _make_master()
    client_user = _make_client()
    job = _completed_job(client_user, master)

    api = APIClient()
    api.force_authenticate(client_user)
    with mock.patch(NOTIFY_PATH) as notify:
        resp = api.post(
            "/api/v1/reviews/",
            {"job": job.id, "rating": 5, "text": "Ajoyib usta!", "recommend": True},
            format="json",
        )
    assert resp.status_code == 201, resp.content
    assert resp.data["rating"] == 5
    assert resp.data["master"] == master.id
    review = Review.objects.get(job=job)
    assert review.author_id == client_user.id
    assert review.master_id == master.id
    notify.assert_called_once()


def test_second_review_on_same_job_rejected():
    master = _make_master()
    client_user = _make_client()
    job = _completed_job(client_user, master)
    Review.objects.create(job=job, author=client_user, master=master, rating=4)

    api = APIClient()
    api.force_authenticate(client_user)
    with mock.patch(NOTIFY_PATH):
        resp = api.post(
            "/api/v1/reviews/",
            {"job": job.id, "rating": 3, "text": "Ikkinchi sharh"},
            format="json",
        )
    assert resp.status_code == 400
    assert Review.objects.filter(job=job).count() == 1


def test_review_cannot_be_left_on_non_completed_job():
    master = _make_master()
    client_user = _make_client()
    job = Job.objects.create(
        client=client_user,
        title="Open ish",
        description="Hali yakunlanmagan.",
        status=JobStatus.OPEN,
        assigned_master=master,
    )

    api = APIClient()
    api.force_authenticate(client_user)
    with mock.patch(NOTIFY_PATH):
        resp = api.post(
            "/api/v1/reviews/",
            {"job": job.id, "rating": 5},
            format="json",
        )
    assert resp.status_code == 400


def test_master_aggregates_update_after_review_signal():
    master = _make_master()
    client_user = _make_client()
    job = _completed_job(client_user, master)

    api = APIClient()
    api.force_authenticate(client_user)
    with mock.patch(NOTIFY_PATH):
        resp = api.post(
            "/api/v1/reviews/",
            {"job": job.id, "rating": 4},
            format="json",
        )
    assert resp.status_code == 201
    master.refresh_from_db()
    assert master.reviews_count == 1
    assert float(master.rating_avg) == 4.0


def test_list_is_public_and_filterable_by_master():
    master = _make_master()
    client_user = _make_client()
    job = _completed_job(client_user, master)
    Review.objects.create(job=job, author=client_user, master=master, rating=5)

    api = APIClient()  # anonymous
    resp = api.get("/api/v1/reviews/", {"master": master.id})
    assert resp.status_code == 200
    assert resp.data["count"] == 1


def test_master_cannot_create_review():
    master = _make_master()
    other_master = _make_master_other()
    job = _completed_job(other_master.user, master)

    api = APIClient()
    api.force_authenticate(master.user)
    resp = api.post(
        "/api/v1/reviews/",
        {"job": job.id, "rating": 5},
        format="json",
    )
    assert resp.status_code == 403


def _make_master_other():
    user = User.objects.create_user(
        email="usta2@example.com", password="pw12345", role="usta"
    )
    return MasterProfile.objects.create(user=user)
