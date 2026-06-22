"""Institution viewsets."""

from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.institutions.api.serializers import DepartmentSerializer, InstitutionSerializer
from apps.institutions.models import Department, Institution
from apps.institutions.permissions import IsInstitutionAdminOrReadOnly


@extend_schema(tags=["institutions"])
class InstitutionViewSet(ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsInstitutionAdminOrReadOnly]


@extend_schema(tags=["institutions"])
class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.select_related("institution")
    serializer_class = DepartmentSerializer
    permission_classes = [IsInstitutionAdminOrReadOnly]
