"""Application selectors."""

from apps.applications.models import Application
from apps.common.models import UserRole


def application_list_for_user(user):
    qs = Application.objects.select_related("offer", "offer__company", "student", "reviewed_by")
    if user.role == UserRole.STUDENT:
        return qs.filter(student=user)
    if user.role == UserRole.COMPANY_MEMBER:
        return qs.filter(offer__company__memberships__user=user).distinct()
    return qs
