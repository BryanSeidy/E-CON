"""Company domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import BaseSoftDeleteModel


class Company(BaseSoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class CompanyMembership(BaseSoftDeleteModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_memberships"
    )
    title = models.CharField(max_length=150, blank=True)
    is_owner = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["company", "user"], name="unique_company_member")
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.company}"
