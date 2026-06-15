"""Keep each Job's full-text search_vector in sync with its text.

Uses the ``simple`` text-search config (no language stemming) so it works
uniformly for Uzbek / Russian / English content. The recompute runs through
``.update()``, which does not re-fire ``post_save`` — so there is no recursion.
"""
from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Job

# Title matches outrank description matches.
JOB_SEARCH_VECTOR = SearchVector("title", weight="A", config="simple") + SearchVector(
    "description", weight="B", config="simple"
)


def recompute_job_search_vector(job_id) -> None:
    Job.objects.filter(pk=job_id).update(search_vector=JOB_SEARCH_VECTOR)


@receiver(post_save, sender=Job)
def on_job_saved(sender, instance, **kwargs):
    # `update_fields` that doesn't touch the searchable text → skip the rebuild.
    update_fields = kwargs.get("update_fields")
    if update_fields is not None and not ({"title", "description"} & set(update_fields)):
        return
    recompute_job_search_vector(instance.pk)
