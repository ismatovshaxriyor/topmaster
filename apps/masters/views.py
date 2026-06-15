"""Views for the masters app: public catalog + master self-service."""
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F, Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.common.geo import apply_nearby, nearby_parameters
from apps.common.permissions import IsMaster

from .filters import MasterFilter
from .models import (
    MasterProfile,
    PortfolioItem,
    Skill,
    VerificationDocument,
    VerificationRequest,
)
from .serializers import (
    AvailabilitySerializer,
    DashboardStatsSerializer,
    MasterDetailSerializer,
    MasterProfileUpdateSerializer,
    MasterSummarySerializer,
    OnboardingSerializer,
    PortfolioItemSerializer,
    SkillSerializer,
    VerificationDocumentSerializer,
    VerificationRequestSerializer,
)


@extend_schema(tags=["Masters"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Toʻliq matnli qidiruv (ism, bio, yoʻnalish, koʻnikma boʻyicha).",
            ),
            *nearby_parameters(),
        ]
    )
)
class MasterViewSet(ReadOnlyModelViewSet):
    """Public catalog of masters (list + detail)."""

    permission_classes = [AllowAny]
    queryset = (
        MasterProfile.objects.select_related("user", "user__city")
        .prefetch_related("categories", "skills", "portfolio")
    )
    filterset_class = MasterFilter
    ordering_fields = ["rating_avg", "reviews_count", "min_price", "experience_years"]
    serializer_class = MasterSummarySerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MasterDetailSerializer
        return MasterSummarySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        if q and self.action == "list":
            # Rank over the master's own text (name + bio); category and skill
            # hits are matched too. Rank depends only on to-one fields, so
            # distinct() collapses the join duplicates without losing ordering.
            vector = SearchVector(
                "user__full_name", weight="A", config="simple"
            ) + SearchVector("bio", weight="B", config="simple")
            query = SearchQuery(q, config="simple", search_type="websearch")
            qs = (
                qs.annotate(rank=SearchRank(vector, query))
                .filter(
                    Q(rank__gt=0)
                    | Q(categories__label__icontains=q)
                    | Q(skills__title__icontains=q)
                )
                .distinct()
                .order_by("-is_top", "-rank", "-rating_avg")
            )
        if self.action == "list":
            # Nearby search (?lat&lng[&radius_km]); precise coords fall back to
            # the master's city. When applied, results are ordered by distance.
            qs, _ = apply_nearby(
                qs,
                self.request,
                Coalesce(F("latitude"), F("user__city__latitude")),
                Coalesce(F("longitude"), F("user__city__longitude")),
            )
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        MasterProfile.objects.filter(pk=instance.pk).update(
            views_count=F("views_count") + 1
        )
        instance.refresh_from_db(fields=["views_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=["Masters"])
class MasterMeView(RetrieveUpdateAPIView):
    """The authenticated master's own profile."""

    permission_classes = [IsMaster]
    queryset = MasterProfile.objects.all()
    serializer_class = MasterDetailSerializer

    def get_object(self):
        return self.request.user.master_profile

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return MasterProfileUpdateSerializer
        return MasterDetailSerializer


@extend_schema(tags=["Masters"])
class AvailabilityView(UpdateAPIView):
    """PATCH availability status on own profile."""

    permission_classes = [IsMaster]
    queryset = MasterProfile.objects.all()
    serializer_class = AvailabilitySerializer

    def get_object(self):
        return self.request.user.master_profile


@extend_schema(tags=["Masters"])
class SkillViewSet(ModelViewSet):
    """CRUD over the authenticated master's skills."""

    permission_classes = [IsMaster]
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

    def get_queryset(self):
        return self.request.user.master_profile.skills.all()

    def perform_create(self, serializer):
        serializer.save(master=self.request.user.master_profile)


@extend_schema(tags=["Masters"])
class PortfolioViewSet(ModelViewSet):
    """CRUD over the authenticated master's portfolio (image upload)."""

    permission_classes = [IsMaster]
    serializer_class = PortfolioItemSerializer
    queryset = PortfolioItem.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return self.request.user.master_profile.portfolio.all()

    def perform_create(self, serializer):
        serializer.save(master=self.request.user.master_profile)


@extend_schema(tags=["Masters"])
class VerificationView(APIView):
    """Master verification: read status, submit, upload documents."""

    permission_classes = [IsMaster]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = VerificationRequestSerializer

    def _get_request(self):
        master = self.request.user.master_profile
        obj, _ = VerificationRequest.objects.get_or_create(master=master)
        return obj

    @extend_schema(responses=VerificationRequestSerializer)
    def get(self, request, *args, **kwargs):
        obj = self._get_request()
        return Response(VerificationRequestSerializer(obj).data)

    @extend_schema(request=None, responses=VerificationRequestSerializer)
    def post(self, request, *args, **kwargs):
        obj = self._get_request()
        obj.status = VerificationRequest.Status.PENDING
        obj.submitted_at = timezone.now()
        obj.save(update_fields=["status", "submitted_at", "updated_at"])
        return Response(VerificationRequestSerializer(obj).data)


@extend_schema(tags=["Masters"])
class VerificationDocumentView(APIView):
    """Upload / replace a single verification document."""

    permission_classes = [IsMaster]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = VerificationDocumentSerializer

    @extend_schema(
        request=inline_serializer(
            name="VerificationDocUploadRequest",
            fields={
                "doc_type": serializers.ChoiceField(
                    choices=[
                        ("id", "Pasport / ID karta"),
                        ("selfie", "Selfi tekshiruvi"),
                        ("diploma", "Diplom / Sertifikat"),
                        ("address", "Manzil tasdigʻi"),
                    ]
                ),
                "file": serializers.FileField(),
            },
        ),
        responses=VerificationDocumentSerializer,
    )
    def post(self, request, *args, **kwargs):
        master = request.user.master_profile
        vreq, _ = VerificationRequest.objects.get_or_create(master=master)
        doc_type = request.data.get("doc_type")
        if doc_type not in VerificationDocument.DocType.values:
            return Response(
                {"doc_type": "Notoʻgʻri hujjat turi."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )
        file = request.data.get("file")
        doc, _ = VerificationDocument.objects.update_or_create(
            request=vreq,
            doc_type=doc_type,
            defaults={"file": file, "state": VerificationDocument.State.UPLOADED},
        )
        return Response(
            VerificationDocumentSerializer(doc).data,
            status=http_status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Masters"])
class OnboardingView(APIView):
    """First-run setup applied to the authenticated master's profile."""

    permission_classes = [IsMaster]
    serializer_class = OnboardingSerializer

    @extend_schema(request=OnboardingSerializer, responses=MasterDetailSerializer)
    def post(self, request, *args, **kwargs):
        master = request.user.master_profile
        serializer = OnboardingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(master, serializer.validated_data)
        return Response(
            MasterDetailSerializer(master, context={"request": request}).data
        )


@extend_schema(tags=["Masters"])
class DashboardStatsView(APIView):
    """Aggregate numbers for the master dashboard home."""

    permission_classes = [IsMaster]
    serializer_class = DashboardStatsSerializer

    @extend_schema(responses=DashboardStatsSerializer)
    def get(self, request, *args, **kwargs):
        from apps.jobs.models import JobStatus
        from apps.proposals.models import Proposal

        master = request.user.master_profile
        assigned = master.assigned_jobs.all()
        data = {
            "total_orders": assigned.count(),
            "completed": assigned.filter(status=JobStatus.COMPLETED).count(),
            "rating_avg": master.rating_avg,
            "views": master.views_count,
            "new_proposals": Proposal.objects.filter(
                master=master, status=Proposal.Status.PENDING
            ).count(),
        }
        return Response(DashboardStatsSerializer(data).data)
