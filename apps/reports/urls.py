"""Report routes, mounted at /api/v1/reports/."""
from rest_framework.routers import DefaultRouter

from .views import ReportViewSet

router = DefaultRouter()
router.register("", ReportViewSet, basename="report")

urlpatterns = router.urls
