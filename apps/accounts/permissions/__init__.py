"""Account API permissions."""

from rest_framework.permissions import BasePermission

from apps.common.models import UserRole


class IsUniversityStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role
            in {
                UserRole.SUPER_ADMIN,
                UserRole.UNIVERSITY_ADMIN,
                UserRole.HEAD_OF_PROGRAM,
                UserRole.ACADEMIC_SUPERVISOR,
            }
        )
