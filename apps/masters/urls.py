"""URL routes for the masters app (mounted at /api/v1/masters/)."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AvailabilityView,
    DashboardStatsView,
    MasterMeView,
    MasterViewSet,
    OnboardingView,
    PortfolioViewSet,
    SkillViewSet,
    VerificationDocumentView,
    VerificationView,
)

router = DefaultRouter()
router.register("", MasterViewSet, basename="master")

skill_router = DefaultRouter()
skill_router.register("", SkillViewSet, basename="master-skill")

portfolio_router = DefaultRouter()
portfolio_router.register("", PortfolioViewSet, basename="master-portfolio")

urlpatterns = [
    path("me/", MasterMeView.as_view(), name="master-me"),
    path("me/availability/", AvailabilityView.as_view(), name="master-availability"),
    path("me/onboarding/", OnboardingView.as_view(), name="master-onboarding"),
    path("me/verification/", VerificationView.as_view(), name="master-verification"),
    path(
        "me/verification/documents/",
        VerificationDocumentView.as_view(),
        name="master-verification-documents",
    ),
    path("me/dashboard/", DashboardStatsView.as_view(), name="master-dashboard"),
    path("me/skills/", include(skill_router.urls)),
    path("me/portfolio/", include(portfolio_router.urls)),
    path("", include(router.urls)),
]
