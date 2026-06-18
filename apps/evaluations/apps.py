"""Django app configuration for evaluations."""

from __future__ import annotations

from django.apps import AppConfig


class EvaluationsConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.evaluations"
