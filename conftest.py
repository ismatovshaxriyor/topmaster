"""Project-wide pytest fixtures.

Deliberately small — most app tests under ``apps/*/tests.py`` are
self-contained and define their own local fixtures. These provide a shared
``api_client`` plus convenience factories for creating client (mijoz) and
master (usta) users so new/cross-app tests don't have to repeat the boilerplate.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APIClient

User = get_user_model()

DEFAULT_PASSWORD = "test-pass-12345"


@pytest.fixture(autouse=True)
def _clear_cache():
    """Reset the cache around every test.

    DRF throttling stores its counters in the cache; without this they bleed
    across tests and trip rate limits in unrelated cases. Clearing both before
    and after keeps each test's throttle state isolated.
    """
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client():
    """An unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture
def make_client(db):
    """Factory: create a client (mijoz) user.

    Usage::

        user = make_client()
        other = make_client(email="x@example.com", full_name="X")
    """
    counter = {"n": 0}

    def _make(email=None, password=DEFAULT_PASSWORD, **extra):
        counter["n"] += 1
        email = email or f"mijoz{counter['n']}@example.com"
        extra.setdefault("full_name", "Test Mijoz")
        return User.objects.create_user(
            email=email, password=password, role="mijoz", **extra
        )

    return _make


@pytest.fixture
def make_master(db):
    """Factory: create a master (usta) user and its MasterProfile.

    Returns the ``MasterProfile``; the underlying ``User`` is ``profile.user``.
    Any keyword args are forwarded to ``create_user``.
    """
    from apps.masters.models import MasterProfile

    counter = {"n": 0}

    def _make(email=None, password=DEFAULT_PASSWORD, profile_kwargs=None, **extra):
        counter["n"] += 1
        email = email or f"usta{counter['n']}@example.com"
        extra.setdefault("full_name", "Test Usta")
        user = User.objects.create_user(
            email=email, password=password, role="usta", **extra
        )
        return MasterProfile.objects.create(user=user, **(profile_kwargs or {}))

    return _make
