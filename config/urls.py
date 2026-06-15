"""
TopMaster — root URL configuration.

All API routes live under /api/v1/. Each app exposes its own urls module
(apps.<app>.urls) with an `urlpatterns` list. OpenAPI schema + Swagger UI
are served by drf-spectacular.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from apps.common.admin_views import analytics_dashboard


def healthcheck(_request):
    return JsonResponse({"status": "ok", "service": "topmaster-api"})


api_v1 = [
    path("auth/", include("apps.accounts.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("masters/", include("apps.masters.urls")),
    path("jobs/", include("apps.jobs.urls")),
    path("proposals/", include("apps.proposals.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("chat/", include("apps.chat.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("favorites/", include("apps.favorites.urls")),
    path("support/", include("apps.support.urls")),
    path("reports/", include("apps.reports.urls")),
]

urlpatterns = [
    # Custom staff analytics page — must precede the admin catch-all include.
    path("admin/analytics/", analytics_dashboard, name="admin-analytics"),
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="health"),
    # API (version lives in the path; route names are global, e.g. "auth-login")
    path("api/v1/", include(api_v1)),
    # OpenAPI schema + docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

if settings.DEBUG and not settings.USE_S3:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
