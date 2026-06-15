"""Keep MasterProfile rating aggregates in sync with its reviews."""
from decimal import Decimal

from django.db.models import Avg, Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Review


def recompute_master_rating(master) -> None:
    """Refresh denormalised rating_avg / reviews_count for a master."""
    agg = master.reviews.aggregate(avg=Avg("rating"), count=Count("id"))
    master.rating_avg = Decimal(str(round(agg["avg"] or 0, 2)))
    master.reviews_count = agg["count"] or 0
    master.save(update_fields=["rating_avg", "reviews_count", "updated_at"])


@receiver(post_save, sender=Review)
def on_review_saved(sender, instance, **kwargs):
    recompute_master_rating(instance.master)


@receiver(post_delete, sender=Review)
def on_review_deleted(sender, instance, **kwargs):
    recompute_master_rating(instance.master)
