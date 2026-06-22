"""Tracking services."""

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.common.models import InternshipStatus
from apps.tracking.models import WeeklyLog


def submit_weekly_log(
    *, internship, student, week_start, activities: str, blockers: str = "", next_steps: str = ""
) -> WeeklyLog:
    if internship.status != InternshipStatus.ACTIVE:
        raise ValidationError("Weekly logs can only be submitted for active internships.")
    if internship.student_id != student.id:
        raise ValidationError("Only the assigned student can submit weekly logs.")
    return WeeklyLog.objects.create(
        internship=internship,
        student=student,
        week_start=week_start,
        activities=activities,
        blockers=blockers,
        next_steps=next_steps,
        submitted_at=timezone.now(),
    )
