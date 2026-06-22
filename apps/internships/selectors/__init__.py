"""Internship selectors."""

from apps.common.models import UserRole
from apps.internships.models import Internship


def internship_list_for_user(user):
    qs = Internship.objects.select_related(
        "application", "offer", "student", "company", "academic_supervisor"
    )
    if user.role == UserRole.STUDENT:
        return qs.filter(student=user)
    if user.role == UserRole.COMPANY_MEMBER:
        return qs.filter(company__memberships__user=user).distinct()
    if user.role == UserRole.ACADEMIC_SUPERVISOR:
        return qs.filter(academic_supervisor=user)
    return qs
