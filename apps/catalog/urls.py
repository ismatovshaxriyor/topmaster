"""Catalog URL routes, mounted under /api/v1/catalog/."""
from django.urls import path

from .views import CategoryListAPIView, CityListAPIView

urlpatterns = [
    path("cities/", CityListAPIView.as_view(), name="catalog-city-list"),
    path("categories/", CategoryListAPIView.as_view(), name="catalog-category-list"),
]
