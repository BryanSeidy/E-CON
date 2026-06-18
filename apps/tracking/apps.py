"""Django app configuration for tracking."""

from __future__ import annotations

from django.apps import AppConfig


class TrackingConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tracking"
