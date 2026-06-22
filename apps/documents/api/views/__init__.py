"""Document viewsets."""

from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.documents.api.serializers import DocumentSerializer
from apps.documents.permissions import CanAccessDocuments
from apps.documents.selectors import document_list_for_user
from apps.documents.services import approve_document, reject_document


class DocumentViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [CanAccessDocuments]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return document_list_for_user(self.request.user)

    def perform_create(self, serializer):
        document = serializer.save(uploaded_by=self.request.user)
        document.full_clean()
        document.save()

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        document = approve_document(
            document=self.get_object(),
            reviewed_by=request.user,
            comment=request.data.get("comment", ""),
        )
        return Response(self.get_serializer(document).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        document = reject_document(
            document=self.get_object(),
            reviewed_by=request.user,
            comment=request.data.get("comment", ""),
        )
        return Response(self.get_serializer(document).data)
