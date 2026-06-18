"""Django app configuration for offers."""

from __future__ import annotations

from django.apps import AppConfig


class OffersConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.offers"
