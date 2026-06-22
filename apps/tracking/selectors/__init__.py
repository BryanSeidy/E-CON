"""Tracking selectors."""

from apps.common.models import UserRole
from apps.tracking.models import WeeklyLog


def weekly_log_list_for_user(user):
    qs = WeeklyLog.objects.select_related("internship", "student")
    if user.role == UserRole.STUDENT:
        return qs.filter(student=user)
    if user.role == UserRole.COMPANY_MEMBER:
        return qs.filter(internship__company__memberships__user=user).distinct()
    if user.role == UserRole.ACADEMIC_SUPERVISOR:
        return qs.filter(internship__academic_supervisor=user)
    return qs
