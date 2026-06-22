"""Notification services."""

from django.utils import timezone

from apps.notifications.models import Notification


def notify(*, recipient, title: str, message: str) -> Notification:
    return Notification.objects.create(recipient=recipient, title=title, message=message)


def mark_as_read(*, notification: Notification) -> Notification:
    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save(update_fields=["is_read", "read_at", "updated_at"])
    return notification
