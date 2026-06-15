"""Background tasks for the jobs app."""
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def notify_matching_masters(job_id):
    """Notify masters whose category + city match a newly posted job.

    Best-effort: any failure is logged and swallowed so a posting never fails
    because of a notification hiccup.
    """
    try:
        from apps.masters.models import MasterProfile
        from apps.notifications.services import notify

        from .models import Job

        job = Job.objects.select_related("category", "city").filter(id=job_id).first()
        if job is None or job.category_id is None or job.city_id is None:
            return

        masters = (
            MasterProfile.objects.filter(
                categories=job.category, user__city_id=job.city_id
            )
            .select_related("user")
            .distinct()
        )
        if not masters.exists():
            return

        for master in masters:
            try:
                notify(
                    master.user,
                    type="order",
                    title="Yangi buyurtma",
                    body=job.title,
                    data={"job_id": job.id},
                )
            except Exception:  # noqa: BLE001
                logger.exception("notify_matching_masters: failed for master %s", master.id)
    except Exception:  # noqa: BLE001
        logger.exception("notify_matching_masters failed for job %s", job_id)
