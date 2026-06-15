"""Job board routes (mounted under /api/v1/jobs/)."""
from rest_framework.routers import DefaultRouter

from .views import JobViewSet

router = DefaultRouter()
router.register(r"", JobViewSet, basename="job")

urlpatterns = router.urls
