"""Lightweight tests for the accounts app."""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_register_client():
    client = APIClient()
    resp = client.post(
        reverse("auth-register"),
        {
            "email": "mijoz@example.com",
            "password": "Str0ngPass!42",
            "full_name": "Ali Valiyev",
            "role": "mijoz",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    user = User.objects.get(email="mijoz@example.com")
    assert user.is_client
    assert not hasattr(user, "master_profile")


@pytest.mark.django_db
def test_register_master_creates_profile_and_verification():
    client = APIClient()
    resp = client.post(
        reverse("auth-register"),
        {
            "email": "usta@example.com",
            "password": "Str0ngPass!42",
            "full_name": "Bek Ustakor",
            "role": "usta",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    user = User.objects.get(email="usta@example.com")
    assert user.is_master
    profile = user.master_profile
    verification = profile.verification
    assert verification.status == "none"
    docs = {d.doc_type: d for d in verification.documents.all()}
    assert docs["id"].required is True
    assert docs["selfie"].required is True
    assert docs["diploma"].required is False
    assert docs["address"].required is False
    assert all(d.state == "none" for d in docs.values())


@pytest.mark.django_db
def test_login_returns_tokens_and_user():
    User.objects.create_user(
        email="login@example.com", password="Str0ngPass!42", full_name="Test"
    )
    client = APIClient()
    resp = client.post(
        reverse("auth-login"),
        {"email": "login@example.com", "password": "Str0ngPass!42"},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    body = resp.json()
    assert "access" in body
    assert "refresh" in body
    # UserSummarySerializer is public-safe: it carries id/full_name but never
    # contact details (email/phone live only on the private /auth/me/ endpoint).
    assert body["user"]["full_name"] == "Test"
    assert "email" not in body["user"]
    assert "phone" not in body["user"]


@pytest.mark.django_db
def test_me_requires_auth_and_returns_self():
    user = User.objects.create_user(
        email="me@example.com", password="Str0ngPass!42", full_name="Me User"
    )
    client = APIClient()
    assert client.get(reverse("auth-me")).status_code == 401

    client.force_authenticate(user=user)
    resp = client.get(reverse("auth-me"))
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "me@example.com"
    assert body["has_master_profile"] is False
    assert "settings" in body


@pytest.mark.django_db
def test_patch_settings():
    user = User.objects.create_user(
        email="settings@example.com", password="Str0ngPass!42"
    )
    client = APIClient()
    client.force_authenticate(user=user)
    resp = client.patch(
        reverse("auth-settings"),
        {"notif_push": False, "language": "ru", "theme": "dark"},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    body = resp.json()
    assert body["notif_push"] is False
    assert body["language"] == "ru"
    assert body["theme"] == "dark"


# ── Password reset ────────────────────────────────────────────────
@pytest.mark.django_db
def test_password_reset_request_emails_link():
    from django.core import mail

    User.objects.create_user(email="reset@example.com", password="Old!pass123")
    client = APIClient()
    resp = client.post(
        reverse("auth-password-reset"), {"email": "reset@example.com"}, format="json"
    )
    assert resp.status_code == 200, resp.content
    assert len(mail.outbox) == 1
    body = mail.outbox[0].body
    assert "uid:" in body and "token:" in body
    assert "reset-password" in body  # the deep link


@pytest.mark.django_db
def test_password_reset_request_unknown_email_no_leak():
    from django.core import mail

    client = APIClient()
    resp = client.post(
        reverse("auth-password-reset"), {"email": "nobody@example.com"}, format="json"
    )
    # Identical 200 response, but no email is sent — no account enumeration.
    assert resp.status_code == 200
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_password_reset_confirm_sets_new_password():
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    user = User.objects.create_user(email="conf@example.com", password="Old!pass123")
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    client = APIClient()
    resp = client.post(
        reverse("auth-password-reset-confirm"),
        {"uid": uid, "token": token, "new_password": "Brand!new456"},
        format="json",
    )
    assert resp.status_code == 200, resp.content
    user.refresh_from_db()
    assert user.check_password("Brand!new456")
    # The old password no longer authenticates.
    login = client.post(
        reverse("auth-login"),
        {"email": "conf@example.com", "password": "Old!pass123"},
        format="json",
    )
    assert login.status_code == 401


@pytest.mark.django_db
def test_password_reset_confirm_rejects_bad_token():
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    user = User.objects.create_user(email="bad@example.com", password="Old!pass123")
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    client = APIClient()
    resp = client.post(
        reverse("auth-password-reset-confirm"),
        {"uid": uid, "token": "not-a-valid-token", "new_password": "Brand!new456"},
        format="json",
    )
    assert resp.status_code == 400
    user.refresh_from_db()
    assert user.check_password("Old!pass123")  # unchanged


# ── Throttling ────────────────────────────────────────────────────
@pytest.mark.django_db
def test_login_throttled_after_limit(monkeypatch):
    # DRF binds THROTTLE_RATES at import, so override_settings can't change it;
    # set the throttle's rate directly instead (reverted after the test).
    from apps.common.throttles import LoginRateThrottle

    monkeypatch.setattr(LoginRateThrottle, "rate", "3/min", raising=False)
    User.objects.create_user(email="th@example.com", password="Str0ngPass!42")
    client = APIClient()
    codes = [
        client.post(
            reverse("auth-login"),
            {"email": "th@example.com", "password": "wrong"},
            format="json",
        ).status_code
        for _ in range(4)
    ]
    # First three are processed (401 bad creds); the fourth is rate-limited.
    assert codes[:3] == [401, 401, 401]
    assert codes[3] == 429


# ── Audit log ─────────────────────────────────────────────────────
@pytest.mark.django_db
def test_audit_log_records_changes_and_excludes_password():
    from auditlog.models import LogEntry

    user = User.objects.create_user(
        email="audit@example.com", password="Str0ngPass!42", full_name="Before"
    )
    entries = LogEntry.objects.get_for_object(user)
    create_entry = entries.filter(action=LogEntry.Action.CREATE).first()
    assert create_entry is not None
    assert "password" not in str(create_entry.changes)  # excluded field

    user.full_name = "After"
    user.save(update_fields=["full_name"])
    update_entry = (
        LogEntry.objects.get_for_object(user)
        .filter(action=LogEntry.Action.UPDATE)
        .first()
    )
    assert update_entry is not None
    assert "full_name" in str(update_entry.changes)
