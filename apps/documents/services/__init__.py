"""Document services."""

from apps.documents.models import Document


def submit_document(
    *, internship, uploaded_by, title: str, file=None, comment: str = ""
) -> Document:
    return Document.objects.create(
        internship=internship, uploaded_by=uploaded_by, title=title, file=file, comment=comment
    )
