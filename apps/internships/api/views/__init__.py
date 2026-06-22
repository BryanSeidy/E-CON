"""Internship viewsets."""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.internships.api.serializers import InternshipSerializer
from apps.internships.permissions import CanAccessInternships
from apps.internships.selectors import internship_list_for_user
from apps.internships.services import assign_academic_supervisor, complete_internship


class InternshipViewSet(ModelViewSet):
    serializer_class = InternshipSerializer
    permission_classes = [CanAccessInternships]

    def get_queryset(self):
        return internship_list_for_user(self.request.user)

    @action(detail=True, methods=["post"])
    def assign_supervisor(self, request, pk=None):
        internship = assign_academic_supervisor(
            internship=self.get_object(), supervisor_id=request.data.get("academic_supervisor")
        )
        return Response(self.get_serializer(internship).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        internship = complete_internship(internship=self.get_object())
        return Response(self.get_serializer(internship).data)
