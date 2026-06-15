"""Lightweight tests for the proposals app."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.jobs.models import Job, JobStatus
from apps.masters.models import MasterProfile
from apps.proposals.models import Proposal

User = get_user_model()


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        email="client@example.com", password="pass12345", role="mijoz"
    )


@pytest.fixture
def master_user(db):
    user = User.objects.create_user(
        email="master@example.com", password="pass12345", role="usta"
    )
    MasterProfile.objects.create(user=user)
    return user


@pytest.fixture
def open_job(client_user):
    return Job.objects.create(
        client=client_user,
        title="Rozetka almashtirish",
        description="Oshxonadagi rozetkani almashtirish kerak.",
        status=JobStatus.OPEN,
    )


@pytest.mark.django_db
def test_master_creates_proposal_increments_count(master_user, open_job):
    api = APIClient()
    api.force_authenticate(user=master_user)

    resp = api.post(
        "/api/v1/proposals/",
        {"job": open_job.id, "message": "Bajaraman.", "proposed_price": 150000},
        format="json",
    )
    assert resp.status_code == 201, resp.content

    open_job.refresh_from_db()
    assert open_job.proposals_count == 1
    assert Proposal.objects.filter(
        job=open_job, master=master_user.master_profile
    ).exists()


@pytest.mark.django_db
def test_duplicate_proposal_returns_400(master_user, open_job):
    Proposal.objects.create(job=open_job, master=master_user.master_profile)
    api = APIClient()
    api.force_authenticate(user=master_user)

    resp = api.post(
        "/api/v1/proposals/", {"job": open_job.id}, format="json"
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_client_accepts_proposal_assigns_and_rejects_others(
    client_user, master_user, open_job
):
    # Second master + proposal that should get auto-rejected.
    other_user = User.objects.create_user(
        email="master2@example.com", password="pass12345", role="usta"
    )
    other_master = MasterProfile.objects.create(user=other_user)

    p1 = Proposal.objects.create(job=open_job, master=master_user.master_profile)
    p2 = Proposal.objects.create(job=open_job, master=other_master)

    api = APIClient()
    api.force_authenticate(user=client_user)

    resp = api.post(f"/api/v1/proposals/{p1.id}/accept/", format="json")
    assert resp.status_code == 200, resp.content

    p1.refresh_from_db()
    p2.refresh_from_db()
    open_job.refresh_from_db()

    assert p1.status == Proposal.Status.ACCEPTED
    assert p2.status == Proposal.Status.REJECTED
    assert open_job.status == JobStatus.IN_PROGRESS
    assert open_job.assigned_master_id == master_user.master_profile.id
    assert open_job.events.filter(type="accepted").exists()


@pytest.mark.django_db
def test_non_owner_cannot_accept(master_user, open_job):
    proposal = Proposal.objects.create(job=open_job, master=master_user.master_profile)
    api = APIClient()
    api.force_authenticate(user=master_user)  # master, not job owner

    resp = api.post(f"/api/v1/proposals/{proposal.id}/accept/", format="json")
    assert resp.status_code == 403
