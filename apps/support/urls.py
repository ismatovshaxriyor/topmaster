"""URL routes for the support (help center) app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.support.views import (
    FaqListAPIView,
    FaqTopicListAPIView,
    SupportChatViewSet,
)

router = DefaultRouter()
router.register("chat", SupportChatViewSet, basename="support-chat")

urlpatterns = [
    path("topics/", FaqTopicListAPIView.as_view(), name="support-topics"),
    path("faqs/", FaqListAPIView.as_view(), name="support-faqs"),
    path("", include(router.urls)),
]
