"""Django app configuration for notifications."""

from __future__ import annotations

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notifications"
