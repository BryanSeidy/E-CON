"""Document services."""

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.common.models import DocumentStatus
from apps.documents.models import Document, DocumentType


def submit_document(
    *,
    uploaded_by,
    title: str,
    file,
    internship=None,
    document_type: str = DocumentType.CV,
    comment: str = "",
) -> Document:
    document = Document(
        internship=internship,
        uploaded_by=uploaded_by,
        title=title,
        file=file,
        document_type=document_type,
        comment=comment,
    )
    document.full_clean()
    document.save()
    return document


def approve_document(*, document: Document, reviewed_by, comment: str = "") -> Document:
    if document.status not in {DocumentStatus.UPLOADED, DocumentStatus.IN_REVIEW}:
        raise ValidationError("Only uploaded or in-review documents can be approved.")
    document.status = DocumentStatus.APPROVED
    document.reviewed_by = reviewed_by
    document.reviewed_at = timezone.now()
    if comment:
        document.comment = comment
    document.save(update_fields=["status", "reviewed_by", "reviewed_at", "comment", "updated_at"])
    return document


def reject_document(*, document: Document, reviewed_by, comment: str = "") -> Document:
    if document.status not in {DocumentStatus.UPLOADED, DocumentStatus.IN_REVIEW}:
        raise ValidationError("Only uploaded or in-review documents can be rejected.")
    document.status = DocumentStatus.REJECTED
    document.reviewed_by = reviewed_by
    document.reviewed_at = timezone.now()
    if comment:
        document.comment = comment
    document.save(update_fields=["status", "reviewed_by", "reviewed_at", "comment", "updated_at"])

    from apps.notifications.services import notify

    notify(
        recipient=document.uploaded_by,
        title="Document rejected",
        message=f"Your document '{document.title}' was rejected.",
    )
    return document
