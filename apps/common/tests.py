"""Tests for shared/common functionality (admin analytics dashboard)."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_analytics_requires_staff(client, django_user_model):
    # Anonymous users are bounced to the admin login.
    resp = client.get(reverse("admin-analytics"))
    assert resp.status_code in (301, 302)
    assert "/login" in resp.url or "admin" in resp.url


@pytest.mark.django_db
def test_analytics_renders_for_staff(client, django_user_model):
    staff = django_user_model.objects.create_user(
        email="staff@e.uz", password="Str0ngPass!42", is_staff=True
    )
    client.force_login(staff)
    resp = client.get(reverse("admin-analytics"))
    assert resp.status_code == 200
    # Renders the dashboard (exercises every aggregation against an empty DB).
    assert b"Analitika" in resp.content
    assert b"Buyurtmalar holati" in resp.content


@pytest.mark.django_db
def test_analytics_has_geo_map(client, django_user_model):
    admin = django_user_model.objects.create_superuser(email="ageo@e.uz", password="x")
    client.force_login(admin)
    resp = client.get(reverse("admin-analytics"))
    assert resp.status_code == 200
    assert b"tm-geo-map" in resp.content
    assert b"tm-master-points" in resp.content  # json_script payload


@pytest.mark.django_db
def test_city_admin_change_has_map_picker(client, django_user_model):
    from apps.catalog.models import City

    admin = django_user_model.objects.create_superuser(email="amap@e.uz", password="x")
    client.force_login(admin)
    city = City.objects.create(name="MapCity", slug="mapcity", latitude=41.3, longitude=69.2)
    resp = client.get(f"/admin/catalog/city/{city.id}/change/")
    assert resp.status_code == 200
    assert b"tm-map" in resp.content
    assert b"leaflet" in resp.content.lower()


@pytest.mark.django_db
def test_audit_log_admin_list_and_detail(client, django_user_model):
    from auditlog.models import LogEntry

    admin = django_user_model.objects.create_superuser(email="aadmin@e.uz", password="x")
    client.force_login(admin)
    # Produce an UPDATE entry on an audited model.
    u = django_user_model.objects.create_user(
        email="audited@e.uz", password="p", full_name="Before"
    )
    u.full_name = "After"
    u.save(update_fields=["full_name"])

    assert client.get("/admin/auditlog/logentry/").status_code == 200
    entry = (
        LogEntry.objects.get_for_object(u)
        .filter(action=LogEntry.Action.UPDATE)
        .first()
    )
    resp = client.get(f"/admin/auditlog/logentry/{entry.id}/change/")
    assert resp.status_code == 200
    assert b"Maydon" in resp.content  # the readable change table header
