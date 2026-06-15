"""Lightweight pytest-django tests for the jobs app."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.catalog.models import Category, City
from apps.jobs.models import Job, JobStatus

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture
def city():
    return City.objects.create(name="Toshkent", slug="toshkent")


@pytest.fixture
def category():
    return Category.objects.create(key="electrician", label="Elektrik")


@pytest.fixture
def client_user(city):
    return User.objects.create_user(
        email="mijoz@example.com", password="pass12345", role="mijoz", city=city
    )


@pytest.fixture
def master_user(city):
    return User.objects.create_user(
        email="usta@example.com", password="pass12345", role="usta", city=city
    )


def _job_payload(category, city):
    return {
        "category": category.id,
        "city": city.id,
        "title": "Rozetka almashtirish",
        "description": "Ikki xonadagi rozetkalarni almashtirish kerak.",
        "price_type": "fixed",
        "price_amount": 150000,
        "when_choice": "this_week",
        "urgent": False,
    }


def test_client_can_create_job(client_user, category, city):
    api = APIClient()
    api.force_authenticate(client_user)
    resp = api.post("/api/v1/jobs/", _job_payload(category, city), format="json")
    assert resp.status_code == 201, resp.content
    job = Job.objects.get(id=resp.data["id"])
    assert job.client == client_user
    assert job.status == JobStatus.OPEN
    # A 'created' lifecycle event is recorded.
    assert job.events.filter(type="created").exists()


def test_master_cannot_create_job(master_user, category, city):
    api = APIClient()
    api.force_authenticate(master_user)
    resp = api.post("/api/v1/jobs/", _job_payload(category, city), format="json")
    assert resp.status_code == 403


def test_feed_lists_only_open_by_default(client_user, category, city):
    Job.objects.create(
        client=client_user, category=category, city=city,
        title="Ochiq", description="d", status=JobStatus.OPEN,
    )
    Job.objects.create(
        client=client_user, category=category, city=city,
        title="Yakunlangan", description="d", status=JobStatus.COMPLETED,
    )
    api = APIClient()
    api.force_authenticate(client_user)
    resp = api.get("/api/v1/jobs/")
    assert resp.status_code == 200
    titles = [j["title"] for j in resp.data["results"]]
    assert "Ochiq" in titles
    assert "Yakunlangan" not in titles


def test_owner_can_complete_job(client_user, master_user, category, city):
    master_profile = master_user.master_profile if hasattr(master_user, "master_profile") else None
    job = Job.objects.create(
        client=client_user, category=category, city=city,
        title="Ish", description="d", status=JobStatus.IN_PROGRESS,
        assigned_master=master_profile,
    )
    api = APIClient()
    api.force_authenticate(client_user)
    resp = api.post(f"/api/v1/jobs/{job.id}/complete/")
    assert resp.status_code == 200, resp.content
    job.refresh_from_db()
    assert job.status == JobStatus.COMPLETED
    assert job.events.filter(type="completed").exists()


def test_fulltext_search_q_filters_and_ranks(client_user, category, city):
    Job.objects.create(
        client=client_user, category=category, city=city,
        title="Konditsioner o'rnatish", description="Yangi konditsioner o'rnatish kerak",
        status=JobStatus.OPEN,
    )
    Job.objects.create(
        client=client_user, category=category, city=city,
        title="Devor bo'yash", description="Xonani bo'yash kerak", status=JobStatus.OPEN,
    )
    api = APIClient()
    api.force_authenticate(client_user)
    resp = api.get("/api/v1/jobs/", {"q": "konditsioner"})
    assert resp.status_code == 200, resp.content
    titles = [j["title"] for j in resp.data["results"]]
    assert "Konditsioner o'rnatish" in titles
    assert "Devor bo'yash" not in titles


def test_jobs_nearby_search_filters_by_radius(client_user, category):
    tash = City.objects.create(
        name="JT", slug="jt", latitude=41.2995, longitude=69.2401
    )
    sam = City.objects.create(name="JS", slug="js", latitude=39.6270, longitude=66.9750)
    Job.objects.create(
        client=client_user, category=category, city=tash,
        title="Yaqin ish", description="d", status=JobStatus.OPEN,
    )
    Job.objects.create(
        client=client_user, category=category, city=sam,
        title="Uzoq ish", description="d", status=JobStatus.OPEN,
    )
    api = APIClient()
    api.force_authenticate(client_user)
    resp = api.get("/api/v1/jobs/", {"lat": 41.3, "lng": 69.24, "radius_km": 50})
    assert resp.status_code == 200, resp.content
    titles = [j["title"] for j in resp.data["results"]]
    assert "Yaqin ish" in titles
    assert "Uzoq ish" not in titles
    # The nearby annotation is surfaced.
    near = next(j for j in resp.data["results"] if j["title"] == "Yaqin ish")
    assert near["distance_km"] is not None


def test_non_owner_cannot_complete_job(client_user, category, city):
    other = User.objects.create_user(
        email="other@example.com", password="pass12345", role="mijoz", city=city
    )
    job = Job.objects.create(
        client=client_user, category=category, city=city,
        title="Ish", description="d", status=JobStatus.IN_PROGRESS,
    )
    api = APIClient()
    api.force_authenticate(other)
    resp = api.post(f"/api/v1/jobs/{job.id}/complete/")
    assert resp.status_code == 403
