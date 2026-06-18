"""Django app configuration for documents."""

from __future__ import annotations

from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.documents"
