"""Reusable model mixins."""

from __future__ import annotations

from django.db import models


class ActiveFlagMixin(models.Model):
    """Adds an activation flag for reference/profile records."""

    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class MetadataMixin(models.Model):
    """Adds a flexible JSON metadata field for support tables."""

    metadata = models.JSONField(blank=True, default=dict)

    class Meta:
        abstract = True
