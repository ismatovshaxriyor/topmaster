"""Great-circle (Haversine) distance for nearby-search endpoints.

Runs on vanilla PostgreSQL through Django's math DB functions — no PostGIS,
no extensions. Coordinates are plain degrees (FloatField). Rows with NULL
coordinates produce a NULL distance, which ``distance_km__lte`` filters drop
automatically.
"""
import contextlib

from django.db.models import ExpressionWrapper, FloatField, Value
from django.db.models.functions import ASin, Cos, Power, Radians, Sin, Sqrt

EARTH_RADIUS_KM = 6371.0


def distance_km_expr(lat_field, lng_field, lat, lng):
    """ORM expression: great-circle km from (lat, lng) to each row's coords.

    ``lat_field`` / ``lng_field`` are expressions yielding the row's latitude /
    longitude in degrees — e.g. ``F("latitude")`` or a ``Coalesce`` that falls
    back to the row's city coordinates.
    """
    lat0 = Radians(Value(float(lat)))
    lng0 = Radians(Value(float(lng)))
    row_lat = Radians(lat_field)
    row_lng = Radians(lng_field)
    dlat = ExpressionWrapper(row_lat - lat0, output_field=FloatField())
    dlng = ExpressionWrapper(row_lng - lng0, output_field=FloatField())
    a = Power(Sin(dlat / Value(2.0)), Value(2)) + Cos(lat0) * Cos(row_lat) * Power(
        Sin(dlng / Value(2.0)), Value(2)
    )
    return ExpressionWrapper(
        Value(2.0 * EARTH_RADIUS_KM) * ASin(Sqrt(a)),
        output_field=FloatField(),
    )


def apply_nearby(qs, request, lat_field, lng_field, alias="distance_km"):
    """Annotate ``alias`` with distance and, if ?lat/?lng given, sort by it.

    Optional ?radius_km caps the results. Returns ``(queryset, applied)`` where
    ``applied`` is True when valid coordinates were supplied. When not applied,
    the queryset is returned unchanged so callers keep their default ordering.
    """
    raw_lat = request.query_params.get("lat")
    raw_lng = request.query_params.get("lng")
    if raw_lat in (None, "") or raw_lng in (None, ""):
        return qs, False
    try:
        lat = float(raw_lat)
        lng = float(raw_lng)
    except (TypeError, ValueError):
        return qs, False

    qs = qs.annotate(**{alias: distance_km_expr(lat_field, lng_field, lat, lng)})

    raw_radius = request.query_params.get("radius_km")
    if raw_radius:
        with contextlib.suppress(TypeError, ValueError):
            qs = qs.filter(**{f"{alias}__lte": float(raw_radius)})

    return qs.order_by(alias), True


# OpenAPI query params shared by the nearby-search list endpoints.
def nearby_parameters():
    from drf_spectacular.types import OpenApiTypes
    from drf_spectacular.utils import OpenApiParameter

    return [
        OpenApiParameter(
            "lat", OpenApiTypes.FLOAT, OpenApiParameter.QUERY,
            description="Qidiruv markazi — kenglik (masofa bo'yicha saralash uchun).",
        ),
        OpenApiParameter(
            "lng", OpenApiTypes.FLOAT, OpenApiParameter.QUERY,
            description="Qidiruv markazi — uzunlik.",
        ),
        OpenApiParameter(
            "radius_km", OpenApiTypes.FLOAT, OpenApiParameter.QUERY,
            description="Ixtiyoriy: shu km radius ichidagilarni qaytaradi.",
        ),
    ]
