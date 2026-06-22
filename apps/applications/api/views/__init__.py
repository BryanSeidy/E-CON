"""Application viewsets."""

from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.applications.api.serializers import ApplicationSerializer
from apps.applications.models import Application
from apps.applications.permissions import CanManageApplications
from apps.applications.selectors import application_list_for_user
from apps.applications.services import accept_application, reject_application, submit_application
from apps.internships.api.serializers import InternshipSerializer


@extend_schema(tags=["applications"])
class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.none()
    serializer_class = ApplicationSerializer
    permission_classes = [CanManageApplications]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["offer__title", "offer__company__name", "student__email", "cover_letter"]
    ordering_fields = ["created_at", "reviewed_at", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = application_list_for_user(self.request.user)
        status = self.request.query_params.get("status")
        offer = self.request.query_params.get("offer")
        company = self.request.query_params.get("company")
        if status:
            queryset = queryset.filter(status=status)
        if offer:
            queryset = queryset.filter(offer_id=offer)
        if company:
            queryset = queryset.filter(offer__company_id=company)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            application = submit_application(
                offer=serializer.validated_data["offer"],
                student=request.user,
                cover_letter=serializer.validated_data.get("cover_letter", ""),
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        output = self.get_serializer(application)
        return Response(output.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        try:
            internship = accept_application(application=self.get_object(), reviewed_by=request.user)
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(InternshipSerializer(internship).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        try:
            application = reject_application(
                application=self.get_object(), reviewed_by=request.user
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(self.get_serializer(application).data)
