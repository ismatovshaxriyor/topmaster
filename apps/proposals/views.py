"""Proposal views (takliflar): master applies; client accepts/rejects."""
from django.db import IntegrityError, transaction
from django.db.models import F, Q
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsMaster
from apps.jobs.models import Job, JobEvent, JobStatus

from .models import Proposal
from .serializers import ProposalCreateSerializer, ProposalSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "job",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                required=False,
                description="Buyurtma IDsi boʻyicha filtrlash",
            ),
        ],
    ),
)
@extend_schema(tags=["Proposals"])
class ProposalViewSet(ModelViewSet):
    """CRUD + lifecycle actions for proposals."""

    queryset = Proposal.objects.select_related(
        "job", "master", "master__user", "master__user__city"
    )
    serializer_class = ProposalSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ProposalCreateSerializer
        return ProposalSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsMaster()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset
        if not user.is_authenticated:
            return qs.none()
        master = getattr(user, "master_profile", None)

        # Visibility: a user may see a proposal if they are the proposing master
        # OR they own the job it targets. This also lets a client retrieve a
        # single proposal for the accept/reject detail actions.
        visible = Q(job__client_id=user.id)
        if master is not None:
            visible |= Q(master=master)

        job_id = self.request.query_params.get("job")
        if job_id:
            return qs.filter(visible, job_id=job_id)
        return qs.filter(visible)

    @extend_schema(request=ProposalCreateSerializer, responses=ProposalSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.validated_data["job"]
        if job.status != JobStatus.OPEN:
            raise ValidationError({"job": "Bu buyurtma takliflar uchun ochiq emas."})

        master = request.user.master_profile
        try:
            with transaction.atomic():
                proposal = serializer.save(master=master)
                Job.objects.filter(pk=job.pk).update(
                    proposals_count=F("proposals_count") + 1
                )
        except IntegrityError:
            raise ValidationError(
                {"job": "Siz ushbu buyurtmaga allaqachon taklif yuborgansiz."}
            ) from None

        from apps.notifications.services import notify

        notify(
            job.client,
            type="order",
            title="Yangi taklif",
            body=f"\"{job.title}\" buyurtmangizga yangi taklif keldi.",
            data={"job_id": job.id, "proposal_id": proposal.id},
        )

        out = ProposalSerializer(proposal, context=self.get_serializer_context())
        return Response(out.data, status=status.HTTP_201_CREATED)

    @extend_schema(request=None, responses=ProposalSerializer)
    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        proposal = self.get_object()
        job = proposal.job
        if job.client_id != request.user.id:
            raise PermissionDenied("Faqat buyurtma egasi taklifni qabul qila oladi.")
        if job.status != JobStatus.OPEN:
            raise ValidationError(
                {"job": "Bu buyurtma uchun taklif qabul qilib boʻlmaydi."}
            )
        if proposal.status != Proposal.Status.PENDING:
            raise ValidationError({"status": "Bu taklif kutilayotgan holatda emas."})

        now = timezone.now()
        with transaction.atomic():
            proposal.status = Proposal.Status.ACCEPTED
            proposal.responded_at = now
            proposal.save(update_fields=["status", "responded_at", "updated_at"])

            # Reject all other pending proposals on the same job.
            Proposal.objects.filter(
                job=job, status=Proposal.Status.PENDING
            ).exclude(pk=proposal.pk).update(
                status=Proposal.Status.REJECTED, responded_at=now
            )

            job.assigned_master = proposal.master
            job.status = JobStatus.IN_PROGRESS
            job.save(update_fields=["assigned_master", "status", "updated_at"])

            JobEvent.objects.create(
                job=job, type=JobEvent.EventType.ACCEPTED, actor=request.user
            )

        from apps.notifications.services import notify

        notify(
            proposal.master.user,
            type="accepted",
            title="Taklifingiz qabul qilindi",
            body=f"\"{job.title}\" buyurtmasi boʻyicha taklifingiz qabul qilindi.",
            data={"job_id": job.id, "proposal_id": proposal.id},
        )

        out = ProposalSerializer(proposal, context=self.get_serializer_context())
        return Response(out.data)

    @extend_schema(request=None, responses=ProposalSerializer)
    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        proposal = self.get_object()
        job = proposal.job
        if job.client_id != request.user.id:
            raise PermissionDenied("Faqat buyurtma egasi taklifni rad eta oladi.")
        if proposal.status != Proposal.Status.PENDING:
            raise ValidationError({"status": "Bu taklif kutilayotgan holatda emas."})

        proposal.status = Proposal.Status.REJECTED
        proposal.responded_at = timezone.now()
        proposal.save(update_fields=["status", "responded_at", "updated_at"])

        from apps.notifications.services import notify

        notify(
            proposal.master.user,
            type="rejected",
            title="Taklifingiz rad etildi",
            body=f"\"{job.title}\" buyurtmasi boʻyicha taklifingiz rad etildi.",
            data={"job_id": job.id, "proposal_id": proposal.id},
        )

        out = ProposalSerializer(proposal, context=self.get_serializer_context())
        return Response(out.data)

    @extend_schema(request=None, responses=ProposalSerializer)
    @action(detail=True, methods=["post"])
    def withdraw(self, request, pk=None):
        proposal = self.get_object()
        master = getattr(request.user, "master_profile", None)
        if master is None or proposal.master_id != master.id:
            raise PermissionDenied("Faqat taklif egasi uni qaytarib ola oladi.")
        if proposal.status != Proposal.Status.PENDING:
            raise ValidationError({"status": "Faqat kutilayotgan taklifni qaytarib olish mumkin."})

        proposal.status = Proposal.Status.WITHDRAWN
        proposal.responded_at = timezone.now()
        proposal.save(update_fields=["status", "responded_at", "updated_at"])

        out = ProposalSerializer(proposal, context=self.get_serializer_context())
        return Response(out.data)
