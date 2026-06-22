"""Document viewsets."""

from rest_framework.viewsets import ModelViewSet

from apps.documents.api.serializers import DocumentSerializer
from apps.documents.permissions import CanAccessDocuments
from apps.documents.selectors import document_list_for_user


class DocumentViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [CanAccessDocuments]

    def get_queryset(self):
        return document_list_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
