"""Reusable querysets shared by foundation models."""

from __future__ import annotations

from typing import TypeVar

from django.db import models
from django.utils import timezone

ModelT = TypeVar("ModelT", bound=models.Model)


class SoftDeleteQuerySet(models.QuerySet[ModelT]):
    """QuerySet implementing logical deletion."""

    def alive(self) -> SoftDeleteQuerySet[ModelT]:
        """Return rows that are not logically deleted."""
        return self.filter(is_deleted=False)

    def deleted(self) -> SoftDeleteQuerySet[ModelT]:
        """Return rows that are logically deleted."""
        return self.filter(is_deleted=True)

    def soft_delete(self, *, deleted_by: models.Model | None = None) -> int:
        """Mark every row in the queryset as deleted."""
        updated = self.update(
            is_deleted=True,
            deleted_at=timezone.now(),
            deleted_by=deleted_by,
        )
        return int(updated)

    def restore(self) -> int:
        """Restore every row in the queryset."""
        updated = self.update(
            is_deleted=False,
            deleted_at=None,
            deleted_by=None,
        )
        return int(updated)


class TenantAwareQuerySet(models.QuerySet[ModelT]):
    """QuerySet helpers for logical tenant isolation."""

    def for_university(self, university_id: object) -> TenantAwareQuerySet[ModelT]:
        """Restrict rows to a university identifier."""
        return self.filter(university_id=university_id)

    def for_company(self, company_id: object) -> TenantAwareQuerySet[ModelT]:
        """Restrict rows to a company identifier."""
        return self.filter(company_id=company_id)
