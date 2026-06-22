"""Internship viewsets."""

from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.internships.api.serializers import InternshipSerializer
from apps.internships.models import Internship
from apps.internships.permissions import CanAccessInternships
from apps.internships.selectors import internship_list_for_user
from apps.internships.services import assign_academic_supervisor, complete_internship


@extend_schema(tags=["internships"])
class InternshipViewSet(ModelViewSet):
    queryset = Internship.objects.none()
    serializer_class = InternshipSerializer
    permission_classes = [CanAccessInternships]

    def get_queryset(self):
        return internship_list_for_user(self.request.user)

    @action(detail=True, methods=["post"])
    def assign_supervisor(self, request, pk=None):
        try:
            internship = assign_academic_supervisor(
                internship=self.get_object(), supervisor_id=request.data.get("academic_supervisor")
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(self.get_serializer(internship).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        try:
            internship = complete_internship(internship=self.get_object())
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(self.get_serializer(internship).data)
