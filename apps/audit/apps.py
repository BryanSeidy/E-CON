"""Django app configuration for audit."""

from __future__ import annotations

from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.audit"
