"""Dashboard API endpoints."""

from apps.applications.selectors import application_list_for_user
from apps.common.models import ApplicationStatus, DocumentStatus, InternshipStatus, UserRole
from apps.documents.selectors import document_list_for_user
from apps.internships.selectors import internship_list_for_user
from apps.notifications.selectors import notification_list_for_user
from apps.offers.models import Offer
from apps.tracking.selectors import weekly_log_list_for_user
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

DashboardSummarySerializer = inline_serializer(
    name="DashboardSummary",
    fields={
        "applications": serializers.IntegerField(required=False),
        "pending_applications": serializers.IntegerField(required=False),
        "active_offers": serializers.IntegerField(required=False),
        "assigned_internships": serializers.IntegerField(required=False),
        "active_internships": serializers.IntegerField(required=False),
        "completed_internships": serializers.IntegerField(required=False),
        "documents": serializers.IntegerField(required=False),
        "documents_to_review": serializers.IntegerField(required=False),
        "rejected_documents": serializers.IntegerField(required=False),
        "weekly_logs": serializers.IntegerField(required=False),
        "unread_notifications": serializers.IntegerField(required=False),
    },
)


class RoleDashboardView(APIView):
    """Base class for role-scoped dashboard summaries."""

    allowed_roles: set[str] = set()

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.is_authenticated and request.user.role not in self.allowed_roles:
            self.permission_denied(request, message="Dashboard not available for this role.")


@extend_schema(tags=["dashboard"], responses=DashboardSummarySerializer)
class StudentDashboardView(RoleDashboardView):
    allowed_roles = {UserRole.STUDENT, UserRole.SUPER_ADMIN}

    def get(self, request):
        applications = application_list_for_user(request.user)
        internships = internship_list_for_user(request.user)
        documents = document_list_for_user(request.user)
        return Response(
            {
                "applications": applications.count(),
                "pending_applications": applications.filter(
                    status=ApplicationStatus.PENDING
                ).count(),
                "active_internships": internships.filter(status=InternshipStatus.ACTIVE).count(),
                "documents": documents.count(),
                "rejected_documents": documents.filter(status=DocumentStatus.REJECTED).count(),
                "weekly_logs": weekly_log_list_for_user(request.user).count(),
                "unread_notifications": notification_list_for_user(request.user)
                .filter(is_read=False)
                .count(),
            }
        )


@extend_schema(tags=["dashboard"], responses=DashboardSummarySerializer)
class CompanyDashboardView(RoleDashboardView):
    allowed_roles = {UserRole.COMPANY_MEMBER, UserRole.SUPER_ADMIN}

    def get(self, request):
        company_ids = request.user.company_memberships.values_list("company_id", flat=True)
        applications = application_list_for_user(request.user)
        internships = internship_list_for_user(request.user)
        return Response(
            {
                "active_offers": Offer.objects.filter(
                    company_id__in=company_ids, is_active=True
                ).count(),
                "applications": applications.count(),
                "pending_applications": applications.filter(
                    status=ApplicationStatus.PENDING
                ).count(),
                "active_internships": internships.filter(status=InternshipStatus.ACTIVE).count(),
                "completed_internships": internships.filter(
                    status=InternshipStatus.COMPLETED
                ).count(),
                "unread_notifications": notification_list_for_user(request.user)
                .filter(is_read=False)
                .count(),
            }
        )


@extend_schema(tags=["dashboard"], responses=DashboardSummarySerializer)
class UniversityDashboardView(RoleDashboardView):
    allowed_roles = {
        UserRole.ACADEMIC_SUPERVISOR,
        UserRole.HEAD_OF_PROGRAM,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.SUPER_ADMIN,
    }

    def get(self, request):
        internships = internship_list_for_user(request.user)
        documents = document_list_for_user(request.user)
        return Response(
            {
                "assigned_internships": internships.count(),
                "active_internships": internships.filter(status=InternshipStatus.ACTIVE).count(),
                "completed_internships": internships.filter(
                    status=InternshipStatus.COMPLETED
                ).count(),
                "documents_to_review": documents.filter(status=DocumentStatus.UPLOADED).count(),
                "weekly_logs": weekly_log_list_for_user(request.user).count(),
                "unread_notifications": notification_list_for_user(request.user)
                .filter(is_read=False)
                .count(),
            }
        )
