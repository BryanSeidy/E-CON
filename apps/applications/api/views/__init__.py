"""Application viewsets."""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.applications.api.serializers import ApplicationSerializer
from apps.applications.permissions import CanManageApplications
from apps.applications.selectors import application_list_for_user
from apps.applications.services import accept_application, reject_application
from apps.internships.api.serializers import InternshipSerializer


class ApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [CanManageApplications]

    def get_queryset(self):
        return application_list_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        internship = accept_application(application=self.get_object(), reviewed_by=request.user)
        return Response(InternshipSerializer(internship).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        application = reject_application(application=self.get_object(), reviewed_by=request.user)
        return Response(self.get_serializer(application).data)
