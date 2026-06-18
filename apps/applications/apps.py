"""Django app configuration for applications."""

from __future__ import annotations

from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.applications"
