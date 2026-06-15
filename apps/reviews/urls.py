"""URL routes for the reviews app (mounted at /api/v1/reviews/)."""
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet

router = DefaultRouter()
router.register(r"", ReviewViewSet, basename="review")

urlpatterns = router.urls
