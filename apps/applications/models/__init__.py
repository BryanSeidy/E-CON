"""Application domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import ApplicationStatus, BaseSoftDeleteModel


class Application(BaseSoftDeleteModel):
    offer = models.ForeignKey("offers.Offer", on_delete=models.CASCADE, related_name="applications")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING
    )
    cover_letter = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_applications",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["offer", "student"], name="unique_student_application_per_offer"
            )
        ]

    def __str__(self) -> str:
        return f"{self.student} -> {self.offer}"
