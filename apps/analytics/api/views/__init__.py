"""Analytics API views."""

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analytics.api.serializers import AnalyticsSummarySerializer
from apps.applications.selectors import application_list_for_user
from apps.common.models import UserRole
from apps.documents.selectors import document_list_for_user
from apps.internships.selectors import internship_list_for_user
from apps.notifications.selectors import notification_list_for_user
from apps.offers.selectors import active_offer_list


@extend_schema(tags=["analytics"], responses=AnalyticsSummarySerializer)
class AnalyticsSummaryView(APIView):
    def _offers_queryset(self, user):
        queryset = active_offer_list()
        if user.role == UserRole.COMPANY_MEMBER:
            return queryset.filter(company__memberships__user=user).distinct()
        return queryset

    def get(self, request):
        data = {
            "offers": self._offers_queryset(request.user).count(),
            "applications": application_list_for_user(request.user).count(),
            "internships": internship_list_for_user(request.user).count(),
            "documents": document_list_for_user(request.user).count(),
            "notifications": notification_list_for_user(request.user).count(),
        }
        return Response(AnalyticsSummarySerializer(data).data)
