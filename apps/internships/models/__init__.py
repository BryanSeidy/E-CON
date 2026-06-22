"""Internship domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import BaseSoftDeleteModel, InternshipStatus


class Internship(BaseSoftDeleteModel):
    application = models.OneToOneField(
        "applications.Application", on_delete=models.PROTECT, related_name="internship"
    )
    offer = models.ForeignKey("offers.Offer", on_delete=models.PROTECT, related_name="internships")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="student_internships"
    )
    company = models.ForeignKey(
        "companies.Company", on_delete=models.PROTECT, related_name="internships"
    )
    academic_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="supervised_internships",
    )
    status = models.CharField(
        max_length=20, choices=InternshipStatus.choices, default=InternshipStatus.ASSIGNED
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.student} - {self.company}"
