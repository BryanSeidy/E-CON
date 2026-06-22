"""Document serializers."""

from rest_framework import serializers

from apps.documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "internship",
            "uploaded_by",
            "document_type",
            "title",
            "file",
            "status",
            "comment",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_by",
            "status",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        instance = Document(**attrs)
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            instance.uploaded_by = request.user
        instance.clean()
        return attrs
