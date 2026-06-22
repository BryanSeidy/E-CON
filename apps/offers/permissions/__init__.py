"""Offer permissions."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.common.models import UserRole


class IsOfferReaderOrCompanyMember(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in {UserRole.COMPANY_MEMBER, UserRole.SUPER_ADMIN}
