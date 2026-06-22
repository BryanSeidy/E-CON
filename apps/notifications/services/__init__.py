"""Notification services."""

import logging

from django.utils import timezone

from apps.notifications.models import Notification

logger = logging.getLogger(__name__)


def notify(*, recipient, title: str, message: str) -> Notification | None:
    """Create a notification for the recipient.

    Logs and returns None on failure so that calling business operations
    are not disrupted by notification delivery issues.
    """
    try:
        return Notification.objects.create(recipient=recipient, title=title, message=message)
    except Exception:
        logger.exception(
            "Failed to create notification (recipient=%s, title=%s)",
            getattr(recipient, "id", recipient),
            title,
        )
        return None


def mark_as_read(*, notification: Notification) -> Notification:
    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save(update_fields=["is_read", "read_at", "updated_at"])
    return notification
