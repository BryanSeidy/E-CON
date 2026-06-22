"""Pytest bootstrap for the Django test suite without external plugins."""

from __future__ import annotations

import os

import django
import pytest
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")
django.setup()
call_command("migrate", interactive=False, verbosity=0)


@pytest.fixture(autouse=True)
def clean_database():
    """Keep tests isolated when pytest-django is not installed."""
    yield
    call_command("flush", interactive=False, verbosity=0)
