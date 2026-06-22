"""Institution domain models."""

from __future__ import annotations

from django.db import models

from apps.common.models import BaseSoftDeleteModel


class Institution(BaseSoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=32, unique=True)
    country = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Department(BaseSoftDeleteModel):
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=32)

    class Meta:
        ordering = ["institution__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"], name="unique_department_code_per_institution"
            )
        ]

    def __str__(self) -> str:
        return f"{self.institution} - {self.name}"
