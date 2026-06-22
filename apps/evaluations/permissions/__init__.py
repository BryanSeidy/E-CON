"""Evaluation permissions."""

from rest_framework.permissions import BasePermission

from apps.common.models import UserRole


class CanManageEvaluations(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            in {
                UserRole.COMPANY_MEMBER,
                UserRole.ACADEMIC_SUPERVISOR,
                UserRole.HEAD_OF_PROGRAM,
                UserRole.UNIVERSITY_ADMIN,
                UserRole.SUPER_ADMIN,
            }
        )
