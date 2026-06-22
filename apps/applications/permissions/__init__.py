"""Application permissions."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.common.models import UserRole


class CanManageApplications(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if view.action == "create":
            return request.user.role == UserRole.STUDENT
        return request.user.role in {
            UserRole.STUDENT,
            UserRole.COMPANY_MEMBER,
            UserRole.SUPER_ADMIN,
        }

    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRole.SUPER_ADMIN:
            return True
        if request.user.role == UserRole.STUDENT:
            return request.method in SAFE_METHODS and obj.student_id == request.user.id
        if request.user.role == UserRole.COMPANY_MEMBER:
            return obj.offer.company.memberships.filter(user=request.user).exists()
        return False
