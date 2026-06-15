"""API views for reviews (sharhlar)."""
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.common.permissions import IsClient

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "master",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                required=False,
                description="Sharhlarni usta ID si bo'yicha filtrlash.",
            ),
            OpenApiParameter(
                "job",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                required=False,
                description="Sharhlarni buyurtma (job) ID si bo'yicha filtrlash.",
            ),
        ]
    ),
)
@extend_schema(tags=["Reviews"])
class ReviewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """List reviews (public) and create one (clients only).

    Filter the list by ``?master=<id>`` and optionally ``?job=<id>``.
    """

    queryset = Review.objects.select_related(
        "author", "author__city", "master"
    ).all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["master", "job"]

    def get_permissions(self):
        if self.action == "create":
            return [IsClient()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        return ReviewSerializer

    @extend_schema(request=ReviewCreateSerializer, responses=ReviewSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            review = serializer.save()
        except IntegrityError:
            # OneToOne(job) guards one-per-job at the DB level; turn a race into
            # a clean 400 instead of a 500.
            raise serializers.ValidationError(
                {"job": "Bu buyurtmaga allaqachon sharh qoldirilgan."}
            ) from None
        self._notify_master(review)
        out = ReviewSerializer(review, context=self.get_serializer_context())
        return Response(out.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _notify_master(review):
        # Notify the reviewed master. Rating aggregates are refreshed by a
        # post_save signal, not here.
        from apps.notifications.services import notify

        notify(
            review.master.user,
            type="system",
            title="Yangi sharh",
            body=f"Sizga {review.rating} yulduzli yangi sharh qoldirildi.",
            data={"master_id": review.master_id},
        )
