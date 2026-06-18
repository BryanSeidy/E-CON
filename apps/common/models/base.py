"""Abstract foundation models for the E-CON backend.

No business entity is defined in this module. These abstract models are reused
by later domain models generated in Phase D.3 and beyond.
"""

from __future__ import annotations

import uuid
from typing import Any

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models.managers import AllObjectsManager, SoftDeleteManager


class UUIDModel(models.Model):
    """Abstract model using UUID primary keys for public-safe identifiers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    """Abstract model with creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditModel(models.Model):
    """Abstract fields for lightweight row-level attribution.

    Full business traceability is handled by the audit app in later phases.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_updated",
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Abstract model implementing logical deletion."""

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_deleted",
    )

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def soft_delete(self, *, deleted_by: models.Model | None = None, save: bool = True) -> None:
        """Mark the current instance as logically deleted."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        if save:
            self.save(update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])

    def restore(self, *, save: bool = True) -> None:
        """Restore the current instance from logical deletion."""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        if save:
            self.save(update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])


class TenantAwareModel(models.Model):
    """Abstract marker for tenant-aware entities.

    Domain models should add the concrete university/company foreign keys they
    need. This class centralizes helper behavior without creating fields that
    could force incorrect tenant assumptions on all entities.
    """

    class Meta:
        abstract = True

    def get_tenant_identifiers(self) -> dict[str, Any]:
        """Return available tenant identifiers for permission and audit layers."""
        identifiers: dict[str, Any] = {}
        if hasattr(self, "university_id"):
            identifiers["university_id"] = self.university_id  # type: ignore[attr-defined]
        if hasattr(self, "company_id"):
            identifiers["company_id"] = self.company_id  # type: ignore[attr-defined]
        return identifiers


class BaseModel(UUIDModel, TimestampedModel):
    """Base abstract model for non-soft-deletable domain records."""

    class Meta:
        abstract = True


class BaseSoftDeleteModel(UUIDModel, TimestampedModel, SoftDeleteModel):
    """Base abstract model for soft-deletable domain records."""

    class Meta:
        abstract = True
