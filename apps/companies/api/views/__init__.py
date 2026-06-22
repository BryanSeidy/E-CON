"""Company viewsets."""

from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.companies.api.serializers import CompanyMembershipSerializer, CompanySerializer
from apps.companies.models import Company, CompanyMembership
from apps.companies.permissions import IsCompanyMemberOrAdmin


@extend_schema(tags=["companies"])
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.none()
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyMemberOrAdmin]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "city", "country"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        queryset = Company.objects.all()
        if self.request.user.role == "COMPANY_MEMBER" and self.request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
        }:
            queryset = queryset.filter(memberships__user=self.request.user).distinct()
        return queryset


@extend_schema(tags=["companies"])
class CompanyMembershipViewSet(ModelViewSet):
    queryset = CompanyMembership.objects.none()
    serializer_class = CompanyMembershipSerializer
    permission_classes = [IsCompanyMemberOrAdmin]

    def get_queryset(self):
        queryset = CompanyMembership.objects.select_related("company", "user")
        if self.request.user.role == "COMPANY_MEMBER":
            return queryset.filter(company__memberships__user=self.request.user).distinct()
        return queryset
