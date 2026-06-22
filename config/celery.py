"""Celery application configuration."""

from __future__ import annotations

import os
from pathlib import Path

from celery import Celery


def _load_env_file() -> None:
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_env_file()
if os.getenv("DJANGO_USE_LOCMEM_CACHE", "false").lower() == "true":
    os.environ["CELERY_BROKER_URL"] = "memory://"
    os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("econ")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
