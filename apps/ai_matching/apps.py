"""Django app configuration for ai_matching."""

from __future__ import annotations

from django.apps import AppConfig


class AiMatchingConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ai_matching"
