"""Django app configuration for companies."""

from __future__ import annotations

from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.companies"
