"""Staff-only analytics dashboard rendered inside the Django/Jazzmin admin.

A single read-only KPI page: platform totals, recent growth, the job funnel,
proposal/review health, open reports, top categories/cities and 14-day
sparklines. Linked from the admin top menu ("Analitika").
"""
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone


def _sparkline(qs, today, date_field="created_at", days=14):
    """[(day, count), …] for the last `days`, zero-filled, oldest→newest."""
    start = today - timedelta(days=days - 1)
    rows = (
        qs.filter(**{f"{date_field}__date__gte": start})
        .annotate(d=TruncDate(date_field))
        .values("d")
        .annotate(n=Count("id"))
    )
    counts = {r["d"]: r["n"] for r in rows}
    series = [
        {"day": start + timedelta(days=i), "count": counts.get(start + timedelta(days=i), 0)}
        for i in range(days)
    ]
    peak = max((p["count"] for p in series), default=0) or 1
    for p in series:
        p["pct"] = round(100 * p["count"] / peak)
    return series


@staff_member_required
def analytics_dashboard(request):
    from apps.jobs.models import Job, JobStatus
    from apps.masters.models import MasterProfile
    from apps.proposals.models import Proposal
    from apps.reports.models import Report
    from apps.reviews.models import Review

    User = get_user_model()
    now = timezone.now()
    today = now.date()
    last_7 = now - timedelta(days=7)
    last_30 = now - timedelta(days=30)

    # ── Users ─────────────────────────────────────────────────────
    users = {
        "total": User.objects.count(),
        "clients": User.objects.filter(role="mijoz").count(),
        "masters": User.objects.filter(role="usta").count(),
        "new_today": User.objects.filter(date_joined__date=today).count(),
        "new_7": User.objects.filter(date_joined__gte=last_7).count(),
        "new_30": User.objects.filter(date_joined__gte=last_30).count(),
    }

    # ── Masters ───────────────────────────────────────────────────
    master_status = dict(
        MasterProfile.objects.values_list("status").annotate(n=Count("id"))
    )
    masters = {
        "verified": MasterProfile.objects.filter(is_verified=True).count(),
        "top": MasterProfile.objects.filter(is_top=True).count(),
        "free": master_status.get("free", 0),
        "busy": master_status.get("busy", 0),
        "off": master_status.get("off", 0),
    }

    # ── Jobs funnel ───────────────────────────────────────────────
    by_status = dict(Job.objects.values_list("status").annotate(n=Count("id")))
    jobs = {
        "total": Job.objects.count(),
        "new_today": Job.objects.filter(created_at__date=today).count(),
        "new_7": Job.objects.filter(created_at__gte=last_7).count(),
        "funnel": [
            {"label": label, "count": by_status.get(value, 0)}
            for value, label in JobStatus.choices
        ],
    }

    # ── Proposals & reviews ───────────────────────────────────────
    prop_total = Proposal.objects.count()
    prop_accepted = Proposal.objects.filter(status=Proposal.Status.ACCEPTED).count()
    proposals = {
        "total": prop_total,
        "accepted": prop_accepted,
        "acceptance_rate": round(100 * prop_accepted / prop_total, 1) if prop_total else 0,
    }
    rev = Review.objects.aggregate(n=Count("id"), avg=Avg("rating"))
    reviews = {"total": rev["n"], "avg": round(rev["avg"], 2) if rev["avg"] else 0}

    # ── Reports (trust & safety) ──────────────────────────────────
    reports = {
        "open": Report.objects.filter(
            status__in=[Report.Status.OPEN, Report.Status.REVIEWING]
        ).count(),
        "total": Report.objects.count(),
    }

    # ── Job funnel bar widths (relative to the biggest stage) ─────
    funnel_peak = max((s["count"] for s in jobs["funnel"]), default=0) or 1
    for s in jobs["funnel"]:
        s["pct"] = round(100 * s["count"] / funnel_peak)

    # ── Top categories / cities by job volume ─────────────────────
    def _with_pct(rows, key):
        peak = max((r["n"] for r in rows), default=0) or 1
        for r in rows:
            r["label"] = r[key]
            r["pct"] = round(100 * r["n"] / peak)
        return rows

    top_categories = _with_pct(
        list(
            Job.objects.exclude(category__isnull=True)
            .values("category__label")
            .annotate(n=Count("id"))
            .order_by("-n")[:5]
        ),
        "category__label",
    )
    top_cities = _with_pct(
        list(
            Job.objects.exclude(city__isnull=True)
            .values("city__name")
            .annotate(n=Count("id"))
            .order_by("-n")[:5]
        ),
        "city__name",
    )

    # ── Master geography (city-clustered points for the overview map) ──
    master_points = [
        {
            "name": r["user__city__name"],
            "lat": r["user__city__latitude"],
            "lng": r["user__city__longitude"],
            "count": r["n"],
        }
        for r in (
            MasterProfile.objects.filter(user__city__latitude__isnull=False)
            .values(
                "user__city__name",
                "user__city__latitude",
                "user__city__longitude",
            )
            .annotate(n=Count("id"))
            .order_by("-n")
        )
    ]

    context = {
        "title": "Analitika",
        "users": users,
        "masters": masters,
        "jobs": jobs,
        "proposals": proposals,
        "reviews": reviews,
        "reports": reports,
        "top_categories": top_categories,
        "top_cities": top_cities,
        "jobs_spark": _sparkline(Job.objects, today, "created_at"),
        "users_spark": _sparkline(User.objects, today, "date_joined"),
        "master_points": master_points,
        "generated_at": now,
    }
    return render(request, "admin/analytics.html", context)
