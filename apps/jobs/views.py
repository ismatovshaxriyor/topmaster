"""Job board ViewSet: CRUD, image upload, and lifecycle transitions."""
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F
from django.db.models.functions import Coalesce
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.geo import apply_nearby, nearby_parameters

from .filters import JobFilter
from .models import Job, JobEvent, JobStatus
from .serializers import (
    JobCreateSerializer,
    JobDetailSerializer,
    JobImageSerializer,
    JobListSerializer,
)


@extend_schema(tags=["Jobs"])
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="To'liq matnli qidiruv (sarlavha + tavsif bo'yicha, ahamiyat tartibida).",
            ),
            *nearby_parameters(),
        ]
    )
)
class JobViewSet(viewsets.ModelViewSet):
    """Work orders (buyurtmalar) posted by clients."""

    queryset = Job.objects.select_related(
        "client", "category", "city", "assigned_master__user"
    )
    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = JobFilter
    ordering_fields = ("created_at", "due_date", "price_amount", "urgent")
    # No `ordering` attribute: the model's Meta order is the default, and the
    # full-text branch below sets its own rank ordering without OrderingFilter
    # clobbering it.

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            # Editing is restricted to safe, client-supplied fields — never
            # `status` (which only changes via the lifecycle actions below).
            return JobCreateSerializer
        if self.action == "retrieve":
            return JobDetailSerializer
        return JobListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # Default job board shows only open orders unless a status is requested.
        if self.action == "list" and not self.request.query_params.get("status"):
            qs = qs.filter(status=JobStatus.OPEN)
        # Full-text search (?q=): rank by relevance against the GIN-indexed
        # search_vector. websearch syntax supports quotes and OR/-.
        q = self.request.query_params.get("q")
        if q:
            query = SearchQuery(q, config="simple", search_type="websearch")
            qs = (
                qs.filter(search_vector=query)
                .annotate(rank=SearchRank(F("search_vector"), query))
                .order_by("-rank", "-urgent", "-created_at")
            )
        if self.action == "list":
            # Nearby jobs (?lat&lng[&radius_km]); precise coords fall back to
            # the job's city. When applied, results are ordered by distance.
            qs, _ = apply_nearby(
                qs,
                self.request,
                Coalesce(F("latitude"), F("city__latitude")),
                Coalesce(F("longitude"), F("city__longitude")),
            )
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_client:
            raise PermissionDenied("Faqat mijozlar buyurtma joylashi mumkin.")
        job = serializer.save(client=user)
        JobEvent.objects.create(job=job, type=JobEvent.EventType.CREATED, actor=user)
        from .tasks import notify_matching_masters

        notify_matching_masters.delay(job.id)

    def _get_owned_job(self):
        """Fetch the job and ensure the requester is its client owner."""
        job = self.get_object()
        if job.client_id != self.request.user.id:
            raise PermissionDenied("Bu amal faqat buyurtma egasi uchun.")
        return job

    def perform_update(self, serializer):
        if serializer.instance.client_id != self.request.user.id:
            raise PermissionDenied("Bu amal faqat buyurtma egasi uchun.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.client_id != self.request.user.id:
            raise PermissionDenied("Bu amal faqat buyurtma egasi uchun.")
        instance.delete()

    @extend_schema(responses=JobListSerializer(many=True))
    @action(detail=False, methods=["get"])
    def my_jobs(self, request):
        """Jobs created by the current user."""
        qs = self.filter_queryset(
            self.get_queryset().filter(client=request.user)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = JobListSerializer(page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)
        serializer = JobListSerializer(qs, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @extend_schema(request=JobImageSerializer, responses=JobImageSerializer)
    @action(
        detail=True,
        methods=["post"],
        parser_classes=[MultiPartParser, FormParser],
        serializer_class=JobImageSerializer,
    )
    def images(self, request, pk=None):
        """Attach an image to the job (owner only)."""
        job = self._get_owned_job()
        serializer = JobImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(job=job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={200: JobDetailSerializer, 400: OpenApiResponse(description="Holat mos emas.")},
    )
    @action(detail=True, methods=["post"])
    def mark_awaiting(self, request, pk=None):
        """Assigned master marks work done, awaiting client confirmation."""
        job = self.get_object()
        if not request.user.is_master or job.assigned_master_id is None or (
            job.assigned_master.user_id != request.user.id
        ):
            raise PermissionDenied("Bu amal faqat tayinlangan usta uchun.")
        if job.status != JobStatus.IN_PROGRESS:
            raise ValidationError("Faqat bajarilayotgan buyurtmani tasdiqlashga yuborish mumkin.")
        job.status = JobStatus.AWAITING_CONFIRMATION
        job.save(update_fields=["status", "updated_at"])
        JobEvent.objects.create(job=job, type=JobEvent.EventType.AWAITING, actor=request.user)
        from apps.notifications.services import notify

        notify(
            job.client,
            type="system",
            title="Tasdiqlash kutilmoqda",
            body=job.title,
            data={"job_id": job.id},
        )
        return self._detail_response(job)

    @extend_schema(
        request=None,
        responses={200: JobDetailSerializer, 400: OpenApiResponse(description="Holat mos emas.")},
    )
    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """Client confirms the job is finished."""
        job = self._get_owned_job()
        if job.status not in (JobStatus.IN_PROGRESS, JobStatus.AWAITING_CONFIRMATION):
            raise ValidationError(
                "Faqat bajarilayotgan yoki tasdiqlash kutilayotgan buyurtmani yakunlash mumkin."
            )
        job.status = JobStatus.COMPLETED
        job.save(update_fields=["status", "updated_at"])
        JobEvent.objects.create(job=job, type=JobEvent.EventType.COMPLETED, actor=request.user)
        if job.assigned_master_id is not None:
            from apps.notifications.services import notify

            notify(
                job.assigned_master.user,
                type="system",
                title="Buyurtma yakunlandi",
                body=job.title,
                data={"job_id": job.id},
            )
        return self._detail_response(job)

    @extend_schema(
        request=None,
        responses={200: JobDetailSerializer, 400: OpenApiResponse(description="Holat mos emas.")},
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Client cancels the job (only while not yet completed)."""
        job = self._get_owned_job()
        if job.status == JobStatus.COMPLETED:
            raise ValidationError("Yakunlangan buyurtmani bekor qilib bo'lmaydi.")
        if job.status == JobStatus.CANCELLED:
            raise ValidationError("Buyurtma allaqachon bekor qilingan.")
        job.status = JobStatus.CANCELLED
        job.save(update_fields=["status", "updated_at"])
        JobEvent.objects.create(job=job, type=JobEvent.EventType.CANCELLED, actor=request.user)
        # Reject any still-pending proposals so they cannot later be accepted
        # and silently revive the cancelled order.
        from apps.proposals.models import Proposal

        Proposal.objects.filter(job=job, status=Proposal.Status.PENDING).update(
            status=Proposal.Status.REJECTED, responded_at=timezone.now()
        )
        return self._detail_response(job)

    def _detail_response(self, job):
        serializer = JobDetailSerializer(job, context=self.get_serializer_context())
        return Response(serializer.data)
