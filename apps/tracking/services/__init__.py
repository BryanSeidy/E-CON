"""Tracking services."""

from django.utils import timezone

from apps.tracking.models import WeeklyLog


def submit_weekly_log(
    *, internship, student, week_start, activities: str, blockers: str = "", next_steps: str = ""
) -> WeeklyLog:
    return WeeklyLog.objects.create(
        internship=internship,
        student=student,
        week_start=week_start,
        activities=activities,
        blockers=blockers,
        next_steps=next_steps,
        submitted_at=timezone.now(),
    )
