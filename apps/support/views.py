"""Help-center read endpoints (public) + support chat (authenticated)."""
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.common.throttles import SupportSendRateThrottle
from apps.support import services
from apps.support.models import Faq, FaqTopic, SupportMessage, SupportThread
from apps.support.serializers import (
    FaqSerializer,
    FaqTopicSerializer,
    SupportMessageSerializer,
    SupportSendSerializer,
    SupportThreadSerializer,
)


@extend_schema(tags=["Support"])
class FaqTopicListAPIView(ListAPIView):
    """List FAQ topics with their entries nested."""

    queryset = FaqTopic.objects.prefetch_related("faqs").all()
    serializer_class = FaqTopicSerializer
    permission_classes = (AllowAny,)


@extend_schema(
    tags=["Support"],
    parameters=[
        OpenApiParameter(
            name="topic",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Mavzu kaliti (key) bo'yicha filtrlash",
        )
    ],
)
class FaqListAPIView(ListAPIView):
    """List FAQ entries, optionally filtered by ?topic=<key>."""

    queryset = Faq.objects.select_related("topic").all()
    serializer_class = FaqSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        qs = super().get_queryset()
        topic = self.request.query_params.get("topic")
        if topic:
            qs = qs.filter(topic__key=topic)
        return qs


@extend_schema(tags=["Support"])
class SupportChatViewSet(viewsets.GenericViewSet):
    """User-side support chat. The support team replies from the Django admin."""

    permission_classes = (IsAuthenticated,)
    serializer_class = SupportThreadSerializer

    def _active_thread(self, user, create=True, subject=""):
        thread = (
            SupportThread.objects.filter(
                user=user, status__in=[SupportThread.Status.OPEN, SupportThread.Status.PENDING]
            )
            .order_by("-updated_at")
            .first()
        )
        if thread is None and create:
            thread = SupportThread.objects.create(user=user, subject=subject)
        return thread

    @extend_schema(responses=SupportThreadSerializer)
    @action(detail=False, methods=["get"])
    def thread(self, request):
        """Get (or open) the user's active support thread."""
        thread = self._active_thread(request.user)
        return Response(SupportThreadSerializer(thread).data)

    @extend_schema(responses=SupportMessageSerializer(many=True))
    @action(detail=False, methods=["get"])
    def messages(self, request):
        """Paginated messages of the user's active thread; marks replies read."""
        thread = self._active_thread(request.user, create=False)
        if thread is None:
            return Response({"count": 0, "next": None, "previous": None, "results": []})
        services.mark_staff_messages_read(thread)
        qs = thread.messages.order_by("created_at")
        page = self.paginate_queryset(qs)
        ser = SupportMessageSerializer(page if page is not None else qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @extend_schema(request=SupportSendSerializer, responses=SupportMessageSerializer)
    @action(
        detail=False,
        methods=["post"],
        throttle_classes=[SupportSendRateThrottle],
    )
    def send(self, request):
        """Send a message to support (opens/reopens a thread as needed)."""
        ser = SupportSendSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        thread = self._active_thread(request.user, subject=ser.validated_data.get("subject", ""))
        if not thread.subject and ser.validated_data.get("subject"):
            thread.subject = ser.validated_data["subject"]
            thread.save(update_fields=["subject", "updated_at"])
        message = SupportMessage.objects.create(
            thread=thread, sender=request.user, is_staff=False,
            text=ser.validated_data["text"],
        )
        services.register_user_message(thread, message)
        return Response(SupportMessageSerializer(message).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=None, responses=SupportThreadSerializer)
    @action(detail=False, methods=["post"])
    def read(self, request):
        """Mark the support team's replies as read."""
        thread = self._active_thread(request.user, create=False)
        if thread is not None:
            services.mark_staff_messages_read(thread)
            return Response(SupportThreadSerializer(thread).data)
        return Response({"detail": "Faol suhbat yo'q."}, status=status.HTTP_404_NOT_FOUND)
