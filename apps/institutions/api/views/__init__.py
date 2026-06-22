"""Institution viewsets."""

from rest_framework.viewsets import ModelViewSet

from apps.institutions.api.serializers import DepartmentSerializer, InstitutionSerializer
from apps.institutions.models import Department, Institution
from apps.institutions.permissions import IsInstitutionAdminOrReadOnly


class InstitutionViewSet(ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsInstitutionAdminOrReadOnly]


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.select_related("institution")
    serializer_class = DepartmentSerializer
    permission_classes = [IsInstitutionAdminOrReadOnly]
