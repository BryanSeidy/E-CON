"""Document domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import BaseSoftDeleteModel, DocumentStatus


class Document(BaseSoftDeleteModel):
    internship = models.ForeignKey(
        "internships.Internship", on_delete=models.CASCADE, related_name="documents"
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="uploaded_documents"
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/%Y/%m/", blank=True)
    status = models.CharField(
        max_length=20, choices=DocumentStatus.choices, default=DocumentStatus.UPLOADED
    )
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
