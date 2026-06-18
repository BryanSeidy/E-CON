"""Django app configuration for internships."""

from __future__ import annotations

from django.apps import AppConfig


class InternshipsConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.internships"
