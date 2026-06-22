"""Institution permissions."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.common.models import UserRole


class IsInstitutionAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in {UserRole.UNIVERSITY_ADMIN, UserRole.SUPER_ADMIN}
        )
