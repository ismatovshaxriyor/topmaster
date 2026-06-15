"""Public read-only catalog endpoints: cities and service categories."""
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Category, City
from .serializers import CategorySerializer, CitySerializer


@extend_schema(tags=["Catalog"])
class CityListAPIView(ListAPIView):
    """List all served cities (public)."""

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (AllowAny,)


@extend_schema(tags=["Catalog"])
class CategoryListAPIView(ListAPIView):
    """List active service categories (public)."""

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
