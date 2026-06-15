"""Lightweight tests for the support (help center) endpoints."""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.support.models import Faq, FaqTopic


@pytest.fixture
def seeded():
    orders = FaqTopic.objects.create(key="orders", label="Buyurtmalar", icon="clipboard-list", order=0)
    payments = FaqTopic.objects.create(key="payments", label="To'lovlar", icon="wallet", order=1)
    Faq.objects.create(topic=orders, question="Qanday buyurtma beraman?", answer="...", order=0)
    Faq.objects.create(topic=orders, question="Bekor qila olamanmi?", answer="...", order=1)
    Faq.objects.create(topic=payments, question="To'lov usullari?", answer="...", order=0)
    return {"orders": orders, "payments": payments}


@pytest.mark.django_db
def test_topics_list_public_with_nested_faqs(seeded):
    client = APIClient()
    resp = client.get(reverse("support-topics"))
    assert resp.status_code == 200
    body = resp.json()  # paginated: {count, next, previous, results}
    assert body["count"] == 2
    data = body["results"]
    orders = next(t for t in data if t["key"] == "orders")
    assert orders["label"] == "Buyurtmalar"
    assert len(orders["faqs"]) == 2


@pytest.mark.django_db
def test_faqs_list_public(seeded):
    client = APIClient()
    resp = client.get(reverse("support-faqs"))
    assert resp.status_code == 200
    assert resp.json()["count"] == 3


@pytest.mark.django_db
def test_faqs_filter_by_topic(seeded):
    client = APIClient()
    resp = client.get(reverse("support-faqs"), {"topic": "orders"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 2
    assert all("question" in f for f in body["results"])


@pytest.mark.django_db
def test_seed_command_idempotent():
    from django.core.management import call_command

    from apps.support.management.commands.seed_support import FAQ_TOPICS, FAQS

    call_command("seed_support")
    first = FaqTopic.objects.count(), Faq.objects.count()
    call_command("seed_support")
    assert (FaqTopic.objects.count(), Faq.objects.count()) == first
    # Seed populates exactly the module's topic/FAQ lists.
    assert first == (len(FAQ_TOPICS), len(FAQS))


# ── Support chat ──────────────────────────────────────────────────
@pytest.mark.django_db
def test_support_chat_send_creates_thread_and_message():
    from django.contrib.auth import get_user_model

    user = get_user_model().objects.create_user(email="sc1@e.uz", password="Str0ngPass!42")
    client = APIClient()
    client.force_authenticate(user=user)

    resp = client.post(reverse("support-chat-send"), {"text": "Salom, yordam kerak"}, format="json")
    assert resp.status_code == 201, resp.content

    msgs = client.get(reverse("support-chat-messages"))
    assert msgs.status_code == 200
    assert msgs.json()["count"] == 1  # paginated

    # Anonymous users cannot use support chat.
    assert APIClient().get(reverse("support-chat-thread")).status_code == 401


@pytest.mark.django_db
def test_support_staff_reply_updates_thread_and_notifies():
    from django.contrib.auth import get_user_model

    from apps.notifications.models import Notification
    from apps.support import services
    from apps.support.models import SupportMessage, SupportThread

    user = get_user_model().objects.create_user(email="sc2@e.uz", password="Str0ngPass!42")
    thread = SupportThread.objects.create(user=user)
    reply = SupportMessage.objects.create(thread=thread, is_staff=True, text="Javob tayyor")

    services.register_staff_reply(reply)

    thread.refresh_from_db()
    assert thread.last_message_id == reply.id
    assert thread.user_unread == 1
    assert thread.status == SupportThread.Status.PENDING
    assert Notification.objects.filter(recipient=user, type="system").exists()


@pytest.mark.django_db
def test_support_send_is_throttled(monkeypatch):
    from django.contrib.auth import get_user_model

    from apps.common.throttles import SupportSendRateThrottle

    # Set the rate directly — DRF binds THROTTLE_RATES at import time.
    monkeypatch.setattr(SupportSendRateThrottle, "rate", "2/min", raising=False)
    user = get_user_model().objects.create_user(email="st@e.uz", password="Str0ngPass!42")
    client = APIClient()
    client.force_authenticate(user=user)
    codes = [
        client.post(
            reverse("support-chat-send"), {"text": f"msg {i}"}, format="json"
        ).status_code
        for i in range(3)
    ]
    assert codes[:2] == [201, 201]
    assert codes[2] == 429
