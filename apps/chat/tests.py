"""Lightweight tests for the chat app."""
import sys
import types

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.chat.models import Conversation, ConversationParticipant, Message

User = get_user_model()


@pytest.fixture(autouse=True)
def stub_notifications(monkeypatch):
    """Stub apps.notifications.services.notify so chat tests stay self-contained."""
    module = types.ModuleType("apps.notifications.services")
    module.notify = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "apps.notifications.services", module)
    yield


@pytest.fixture(autouse=True)
def silence_broadcast(monkeypatch):
    """Avoid needing a configured channel layer during REST tests."""
    monkeypatch.setattr("apps.chat.views.broadcast", lambda *a, **k: None)
    yield


def make_user(email):
    return User.objects.create_user(email=email, password="pass12345!")


def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_open_creates_conversation_between_two_users():
    alice = make_user("alice@example.com")
    bob = make_user("bob@example.com")
    client = auth_client(alice)

    resp = client.post("/api/v1/chat/conversations/open/", {"user": bob.id}, format="json")
    assert resp.status_code == 200
    conv_id = resp.data["id"]

    conv = Conversation.objects.get(pk=conv_id)
    assert conv.memberships.count() == 2
    assert set(conv.memberships.values_list("user_id", flat=True)) == {alice.id, bob.id}
    assert resp.data["other"]["id"] == bob.id

    # Opening again returns the same conversation, not a duplicate.
    resp2 = client.post("/api/v1/chat/conversations/open/", {"user": bob.id}, format="json")
    assert resp2.status_code == 200
    assert resp2.data["id"] == conv_id
    assert Conversation.objects.count() == 1


@pytest.mark.django_db
def test_open_rejects_self():
    alice = make_user("alice@example.com")
    client = auth_client(alice)
    resp = client.post("/api/v1/chat/conversations/open/", {"user": alice.id}, format="json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_send_increments_other_participant_unread():
    alice = make_user("alice@example.com")
    bob = make_user("bob@example.com")
    conv = Conversation.objects.create()
    ConversationParticipant.objects.create(conversation=conv, user=alice)
    ConversationParticipant.objects.create(conversation=conv, user=bob)

    client = auth_client(alice)
    resp = client.post(
        f"/api/v1/chat/conversations/{conv.id}/send/", {"text": "Salom"}, format="json"
    )
    assert resp.status_code == 201
    assert resp.data["text"] == "Salom"
    assert resp.data["is_mine"] is True

    conv.refresh_from_db()
    assert conv.last_message_id == resp.data["id"]

    bob_mem = ConversationParticipant.objects.get(conversation=conv, user=bob)
    alice_mem = ConversationParticipant.objects.get(conversation=conv, user=alice)
    assert bob_mem.unread_count == 1
    assert alice_mem.unread_count == 0


@pytest.mark.django_db
def test_messages_endpoint_marks_inbound_read():
    alice = make_user("alice@example.com")
    bob = make_user("bob@example.com")
    conv = Conversation.objects.create()
    ConversationParticipant.objects.create(conversation=conv, user=alice, unread_count=1)
    ConversationParticipant.objects.create(conversation=conv, user=bob)
    msg = Message.objects.create(conversation=conv, sender=bob, text="Assalom")

    client = auth_client(alice)
    resp = client.get(f"/api/v1/chat/conversations/{conv.id}/messages/")
    assert resp.status_code == 200
    results = resp.data.get("results", resp.data)
    assert len(results) == 1
    assert results[0]["is_mine"] is False

    msg.refresh_from_db()
    assert msg.read_at is not None
    alice_mem = ConversationParticipant.objects.get(conversation=conv, user=alice)
    assert alice_mem.unread_count == 0
    assert alice_mem.last_read_at is not None


@pytest.mark.django_db
def test_list_requires_authentication():
    resp = APIClient().get("/api/v1/chat/conversations/")
    assert resp.status_code in (401, 403)


@pytest.mark.django_db
def test_list_only_shows_own_conversations():
    alice = make_user("alice@example.com")
    bob = make_user("bob@example.com")
    carol = make_user("carol@example.com")

    conv = Conversation.objects.create()
    ConversationParticipant.objects.create(conversation=conv, user=alice)
    ConversationParticipant.objects.create(conversation=conv, user=bob)

    # Conversation alice is not part of.
    other = Conversation.objects.create()
    ConversationParticipant.objects.create(conversation=other, user=bob)
    ConversationParticipant.objects.create(conversation=other, user=carol)

    resp = auth_client(alice).get("/api/v1/chat/conversations/")
    assert resp.status_code == 200
    results = resp.data.get("results", resp.data)
    ids = {c["id"] for c in results}
    assert ids == {conv.id}
