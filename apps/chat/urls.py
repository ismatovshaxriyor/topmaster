"""Chat REST routes, mounted under /api/v1/chat/."""
from rest_framework.routers import DefaultRouter

from .views import ConversationViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

urlpatterns = router.urls
