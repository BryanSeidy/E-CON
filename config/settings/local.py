"""Local development settings."""

import os
from pathlib import Path

_env_file = Path(__file__).resolve().parents[2] / ".env"
if _env_file.exists():
    for _raw_line in _env_file.read_text(encoding="utf-8").splitlines():
        _line = _raw_line.strip()
        if not _line or _line.startswith("#") or "=" not in _line:
            continue
        _key, _, _value = _line.partition("=")
        os.environ.setdefault(_key.strip(), _value.strip())

from .base import *  # noqa: F403

DEBUG = True

if os.getenv("DJANGO_USE_SQLITE", "false").lower() == "true":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

if os.getenv("DJANGO_USE_LOCMEM_CACHE", "false").lower() == "true":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
    CELERY_BROKER_URL = "memory://"
    CELERY_RESULT_BACKEND = "cache+memory://"
    os.environ["CELERY_BROKER_URL"] = CELERY_BROKER_URL
    os.environ["CELERY_RESULT_BACKEND"] = CELERY_RESULT_BACKEND
