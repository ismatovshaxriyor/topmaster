"""Tests for the universal report (trust & safety) app."""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.reports.models import Report


@pytest.mark.django_db
def test_create_report_for_master(make_client, make_master):
    user = make_client()
    master = make_master()
    api = APIClient()
    api.force_authenticate(user)
    resp = api.post(
        reverse("report-list"),
        {
            "target_type": "master",
            "target_id": master.id,
            "reason": "spam",
            "description": "Reklama yuboryapti",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    report = Report.objects.get()
    assert report.reporter == user
    assert report.target == master
    assert report.status == Report.Status.OPEN


@pytest.mark.django_db
def test_report_requires_auth():
    api = APIClient()
    resp = api.post(
        reverse("report-list"),
        {"target_type": "user", "target_id": 1, "reason": "spam"},
        format="json",
    )
    assert resp.status_code == 401


@pytest.mark.django_db
def test_report_invalid_target_type(make_client):
    api = APIClient()
    api.force_authenticate(make_client())
    resp = api.post(
        reverse("report-list"),
        {"target_type": "banana", "target_id": 1, "reason": "spam"},
        format="json",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_report_nonexistent_target(make_client):
    api = APIClient()
    api.force_authenticate(make_client())
    resp = api.post(
        reverse("report-list"),
        {"target_type": "job", "target_id": 999999, "reason": "fraud"},
        format="json",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_duplicate_report_rejected(make_client, make_master):
    api = APIClient()
    api.force_authenticate(make_client())
    master = make_master()
    payload = {"target_type": "master", "target_id": master.id, "reason": "spam"}
    assert api.post(reverse("report-list"), payload, format="json").status_code == 201
    second = api.post(reverse("report-list"), payload, format="json")
    assert second.status_code == 400  # unique constraint -> friendly error


@pytest.mark.django_db
def test_list_only_own_reports(make_client, make_master):
    from django.contrib.contenttypes.models import ContentType

    from apps.masters.models import MasterProfile

    u1 = make_client()
    u2 = make_client()
    master = make_master()
    ct = ContentType.objects.get_for_model(MasterProfile)
    Report.objects.create(reporter=u2, content_type=ct, object_id=master.id, reason="spam")

    api = APIClient()
    api.force_authenticate(u1)
    resp = api.get(reverse("report-list"))
    assert resp.status_code == 200
    assert resp.data["count"] == 0  # u1 sees none of u2's reports
