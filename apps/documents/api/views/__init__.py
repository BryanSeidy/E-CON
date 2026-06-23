"""Document viewsets."""

from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.documents.api.serializers import DocumentSerializer
from apps.documents.models import Document
from apps.documents.permissions import CanAccessDocuments
from apps.documents.selectors import document_list_for_user
from apps.documents.services import approve_document, reject_document


@extend_schema(tags=["documents"])
class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.none()
    serializer_class = DocumentSerializer
    permission_classes = [CanAccessDocuments]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "comment", "uploaded_by__email"]
    ordering_fields = ["created_at", "reviewed_at", "status", "document_type"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = document_list_for_user(self.request.user)
        status = self.request.query_params.get("status")
        document_type = self.request.query_params.get("document_type")
        internship = self.request.query_params.get("internship")
        if status:
            queryset = queryset.filter(status=status)
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        if internship:
            queryset = queryset.filter(internship_id=internship)
        return queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=["post"], parser_classes=[JSONParser, MultiPartParser, FormParser])
    def approve(self, request, pk=None):
        try:
            document = approve_document(
                document=self.get_object(),
                reviewed_by=request.user,
                comment=request.data.get("comment", ""),
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(self.get_serializer(document).data)

    @action(detail=True, methods=["post"], parser_classes=[JSONParser, MultiPartParser, FormParser])
    def reject(self, request, pk=None):
        try:
            document = reject_document(
                document=self.get_object(),
                reviewed_by=request.user,
                comment=request.data.get("comment", ""),
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(self.get_serializer(document).data)
