"""Document domain models."""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from apps.common.models import BaseSoftDeleteModel, DocumentStatus


class DocumentType(models.TextChoices):
    """MVP document categories."""

    CV = "CV", "CV"
    CONVENTION = "CONVENTION", "Convention"
    REPORT = "REPORT", "Report"


def validate_document_file_size(file) -> None:
    """Keep uploaded MVP documents within a local-storage friendly limit."""
    max_size_mb = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Document file size must not exceed {max_size_mb}MB.")


class Document(BaseSoftDeleteModel):
    internship = models.ForeignKey(
        "internships.Internship",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="uploaded_documents"
    )
    document_type = models.CharField(
        max_length=20, choices=DocumentType.choices, default=DocumentType.CV
    )
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to="documents/%Y/%m/",
        validators=[FileExtensionValidator(["pdf", "doc", "docx"]), validate_document_file_size],
    )
    status = models.CharField(
        max_length=20, choices=DocumentStatus.choices, default=DocumentStatus.UPLOADED
    )
    comment = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_documents",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["document_type", "status"])]

    def clean(self) -> None:
        if (
            self.document_type in {DocumentType.CONVENTION, DocumentType.REPORT}
            and not self.internship_id
        ):
            raise ValidationError(
                "Convention and report documents must be attached to an internship."
            )

    def __str__(self) -> str:
        return self.title
