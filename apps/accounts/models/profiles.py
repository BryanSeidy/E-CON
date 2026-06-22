"""Profile models for account holders."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import BaseSoftDeleteModel


class StudentProfile(BaseSoftDeleteModel):
    """Academic profile attached to a student user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    student_number = models.CharField(max_length=64, unique=True)
    university = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=32)
    headline = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    skills_summary = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    class Meta:
        ordering = ["student_number"]
        indexes = [models.Index(fields=["university", "department", "program"])]

    def __str__(self) -> str:
        return self.student_number


class StaffProfile(BaseSoftDeleteModel):
    """University staff profile attached to a non-student user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    university = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    role_scope = models.CharField(max_length=255)

    class Meta:
        ordering = ["university", "department"]
        indexes = [models.Index(fields=["university", "department", "role_scope"])]

    def __str__(self) -> str:
        return f"{self.university} - {self.role_scope}"
