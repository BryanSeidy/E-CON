"""Evaluation permissions."""

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.common.models import UserRole


class CanManageEvaluations(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return request.user.role in {
                UserRole.STUDENT,
                UserRole.COMPANY_MEMBER,
                UserRole.ACADEMIC_SUPERVISOR,
                UserRole.HEAD_OF_PROGRAM,
                UserRole.UNIVERSITY_ADMIN,
                UserRole.SUPER_ADMIN,
            }
        return request.user.role in {
            UserRole.COMPANY_MEMBER,
            UserRole.ACADEMIC_SUPERVISOR,
            UserRole.HEAD_OF_PROGRAM,
            UserRole.UNIVERSITY_ADMIN,
            UserRole.SUPER_ADMIN,
        }

    def has_object_permission(self, request, view, obj):
        if request.user.role in {
            UserRole.SUPER_ADMIN,
            UserRole.UNIVERSITY_ADMIN,
            UserRole.HEAD_OF_PROGRAM,
        }:
            return True
        if request.user.role == UserRole.STUDENT:
            return request.method in SAFE_METHODS and obj.internship.student_id == request.user.id
        if request.user.role == UserRole.COMPANY_MEMBER:
            return obj.internship.company.memberships.filter(user=request.user).exists()
        if request.user.role == UserRole.ACADEMIC_SUPERVISOR:
            return obj.internship.academic_supervisor_id == request.user.id
        return False
