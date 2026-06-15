"""URL routes for the favorites app."""
from rest_framework.routers import DefaultRouter

from .views import SavedMasterViewSet

router = DefaultRouter()
router.register(r"", SavedMasterViewSet, basename="saved")

urlpatterns = router.urls
