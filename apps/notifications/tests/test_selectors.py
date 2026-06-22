"""Tests for notification selectors."""

from __future__ import annotations

import pytest

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole
from apps.notifications.models import Notification
from apps.notifications.selectors import notification_list_for_user

pytestmark = pytest.mark.django_db


class TestNotificationListForUser:
    def test_returns_only_own_notifications(self) -> None:
        user = UserFactory(role=UserRole.STUDENT)
        other = UserFactory(role=UserRole.STUDENT)
        Notification.objects.create(recipient=user, title="Mine", message="M")
        Notification.objects.create(recipient=other, title="Theirs", message="T")

        qs = notification_list_for_user(user)
        assert qs.count() == 1
        assert qs.first().title == "Mine"
