"""Institution permissions."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.common.models import UserRole


class IsInstitutionAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in {UserRole.UNIVERSITY_ADMIN, UserRole.SUPER_ADMIN}

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in {UserRole.UNIVERSITY_ADMIN, UserRole.SUPER_ADMIN}
