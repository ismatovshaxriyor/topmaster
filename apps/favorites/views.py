"""Saved (favourite) masters API."""
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsClient

from .models import SavedMaster
from .serializers import SavedMasterCreateSerializer, SavedMasterSerializer


@extend_schema(tags=["Favorites"])
class SavedMasterViewSet(viewsets.ModelViewSet):
    """Manage the authenticated client's saved masters."""

    permission_classes = [IsAuthenticated]
    serializer_class = SavedMasterSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_permissions(self):
        # Saving a master is a client-only action; reads/removes stay open to
        # the authenticated owner.
        if self.action == "create":
            return [IsClient()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return SavedMaster.objects.none()
        return (
            user.saved_masters.select_related("master__user", "master__user__city")
            .all()
        )

    def get_serializer_class(self):
        if self.action == "create":
            return SavedMasterCreateSerializer
        return SavedMasterSerializer

    @extend_schema(
        request=SavedMasterCreateSerializer,
        responses={200: SavedMasterSerializer, 201: SavedMasterSerializer},
    )
    def create(self, request, *args, **kwargs):
        """Save a master. Idempotent: re-saving returns the existing record."""
        write = SavedMasterCreateSerializer(data=request.data)
        write.is_valid(raise_exception=True)
        master = write.validated_data["master"]
        obj, created = SavedMaster.objects.get_or_create(
            client=request.user, master=master
        )
        out = SavedMasterSerializer(obj, context=self.get_serializer_context())
        code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(out.data, status=code)

    @extend_schema(
        responses=inline_serializer(
            name="SavedIdsResponse",
            fields={"ids": serializers.ListField(child=serializers.IntegerField())},
        ),
        description="Saqlangan ustalar identifikatorlari ro'yxati.",
    )
    @action(detail=False, methods=["get"])
    def ids(self, request):
        """Return the list of saved master ids for quick client-side lookups."""
        ids = list(self.get_queryset().values_list("master_id", flat=True))
        return Response({"ids": ids})
