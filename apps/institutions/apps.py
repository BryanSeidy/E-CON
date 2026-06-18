"""Django app configuration for institutions."""

from __future__ import annotations

from django.apps import AppConfig


class InstitutionsConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.institutions"
