"""Reusable managers shared across applications."""

from __future__ import annotations

from typing import Any, TypeVar

from django.db import models

from apps.common.models.querysets import SoftDeleteQuerySet, TenantAwareQuerySet

ModelT = TypeVar("ModelT", bound=models.Model)


class SoftDeleteManager(models.Manager[ModelT]):
    """Default manager that hides logically deleted rows."""

    def get_queryset(self) -> SoftDeleteQuerySet[ModelT]:
        """Return only active rows by default."""
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class AllObjectsManager(models.Manager[ModelT]):
    """Manager exposing all rows, including logically deleted rows."""

    def get_queryset(self) -> SoftDeleteQuerySet[ModelT]:
        """Return all rows."""
        return SoftDeleteQuerySet(self.model, using=self._db)


class TenantAwareManager(models.Manager[ModelT]):
    """Manager exposing tenant filtering helpers."""

    def get_queryset(self) -> TenantAwareQuerySet[ModelT]:
        """Return a tenant-aware queryset."""
        return TenantAwareQuerySet(self.model, using=self._db)

    def for_university(self, university_id: object) -> TenantAwareQuerySet[ModelT]:
        """Restrict rows to a university identifier."""
        return self.get_queryset().for_university(university_id)

    def for_company(self, company_id: object) -> TenantAwareQuerySet[ModelT]:
        """Restrict rows to a company identifier."""
        return self.get_queryset().for_company(company_id)


class SoftDeleteTenantManager(SoftDeleteManager[ModelT]):
    """Manager combining soft-delete defaults and tenant helpers."""

    def for_university(self, university_id: object) -> SoftDeleteQuerySet[ModelT]:
        """Restrict active rows to a university identifier."""
        return self.get_queryset().filter(university_id=university_id)

    def for_company(self, company_id: object) -> SoftDeleteQuerySet[ModelT]:
        """Restrict active rows to a company identifier."""
        return self.get_queryset().filter(company_id=company_id)

    def create(self, **kwargs: Any) -> ModelT:
        """Create a model instance."""
        return super().create(**kwargs)
