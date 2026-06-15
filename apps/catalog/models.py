"""Reference data: cities (shaharlar) and service categories (yo'nalishlar)."""
from django.db import models


class City(models.Model):
    """A city / region served by the platform (e.g. Toshkent, Samarqand)."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    # Geographic centre, used as the fallback location for nearby search when
    # a master/job has no precise coordinates of its own.
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Category(models.Model):
    """A trade / service direction (yo'nalish): Elektrik, Santexnik, …

    `icon` stores a Lucide icon name used by the frontend.
    """

    key = models.SlugField(max_length=40, unique=True)
    label = models.CharField(max_length=80)
    icon = models.CharField(max_length=40, default="wrench")
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "label")
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.label
