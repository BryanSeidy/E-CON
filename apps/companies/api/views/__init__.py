"""Company viewsets."""

from rest_framework.viewsets import ModelViewSet

from apps.companies.api.serializers import CompanyMembershipSerializer, CompanySerializer
from apps.companies.models import Company, CompanyMembership
from apps.companies.permissions import IsCompanyMemberOrAdmin


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsCompanyMemberOrAdmin]


class CompanyMembershipViewSet(ModelViewSet):
    queryset = CompanyMembership.objects.select_related("company", "user")
    serializer_class = CompanyMembershipSerializer
    permission_classes = [IsCompanyMemberOrAdmin]
