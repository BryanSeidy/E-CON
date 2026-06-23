"""Project configuration package.

Keep this package import side-effect free so Django settings can load without
initializing optional worker integrations such as Celery.
"""

from __future__ import annotations

__all__ = ("celery_app",)


def __getattr__(name: str):
    """Lazily expose Celery for callers that explicitly request it."""
    if name == "celery_app":
        from .celery import app as celery_app

        return celery_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
