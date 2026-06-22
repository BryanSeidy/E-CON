"""Notification selectors."""

from apps.notifications.models import Notification


def notification_list_for_user(user):
    return Notification.objects.filter(recipient=user)
