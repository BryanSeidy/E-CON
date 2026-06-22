"""Offer domain models."""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseSoftDeleteModel


class Offer(BaseSoftDeleteModel):
    company = models.ForeignKey(
        "companies.Company", on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    required_skills = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["company", "is_active"])]

    def __str__(self) -> str:
        return self.title
