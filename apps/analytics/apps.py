"""Django app configuration for analytics."""

from __future__ import annotations

from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analytics"
