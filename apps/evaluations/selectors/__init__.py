"""Evaluation selectors."""

from apps.common.models import UserRole
from apps.evaluations.models import Evaluation


def evaluation_list_for_user(user):
    qs = Evaluation.objects.select_related("internship", "evaluator")
    if user.role == UserRole.STUDENT:
        return qs.filter(internship__student=user)
    if user.role == UserRole.COMPANY_MEMBER:
        return qs.filter(internship__company__memberships__user=user).distinct()
    if user.role == UserRole.ACADEMIC_SUPERVISOR:
        return qs.filter(internship__academic_supervisor=user)
    return qs
