"""Application permissions."""

from rest_framework.permissions import BasePermission

from apps.common.models import UserRole


class CanManageApplications(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            in {UserRole.STUDENT, UserRole.COMPANY_MEMBER, UserRole.SUPER_ADMIN}
        )
