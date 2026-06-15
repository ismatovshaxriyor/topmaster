"""Report endpoints: authenticated users file + list their own reports.

Moderation (status changes, resolution) happens in the Django admin, not the
API — keeping the public surface minimal.
"""
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.throttles import ReportRateThrottle

from .models import Report
from .serializers import ReportSerializer


@extend_schema(tags=["Reports"])
class ReportViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """File an abuse report (create) and review your own reports (list)."""

    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReportRateThrottle]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Report.objects.none()
        return (
            Report.objects.filter(reporter=self.request.user)
            .select_related("content_type")
            .order_by("-created_at")
        )
