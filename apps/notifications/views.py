"""API endpoints for managing a user's notifications."""
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


@extend_schema(tags=["Notifications"])
class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """List and manage the authenticated user's notifications."""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.none()

    def get_queryset(self):
        return self.request.user.notifications.all()

    @extend_schema(
        responses=inline_serializer(
            name="UnreadCountResponse",
            fields={"unread": serializers.IntegerField()},
        )
    )
    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        """Return the number of unread notifications."""
        unread = request.user.notifications.filter(read=False).count()
        return Response({"unread": unread})

    @extend_schema(request=None, responses=NotificationSerializer)
    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        """Mark a single notification as read."""
        notification = self.get_object()
        if not notification.read:
            notification.read = True
            notification.save(update_fields=["read"])
        return Response(self.get_serializer(notification).data)

    @extend_schema(
        request=None,
        responses=inline_serializer(
            name="MarkAllReadResponse",
            fields={"updated": serializers.IntegerField()},
        ),
    )
    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        """Mark all of the user's unread notifications as read."""
        updated = request.user.notifications.filter(read=False).update(read=True)
        return Response({"updated": updated}, status=status.HTTP_200_OK)
