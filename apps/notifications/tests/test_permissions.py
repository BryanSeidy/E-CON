"""Tests for notification permissions."""

from __future__ import annotations

import pytest
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole
from apps.notifications.models import Notification
from apps.notifications.permissions import CanAccessOwnNotifications

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


class TestCanAccessOwnNotifications:
    def _perm(self) -> CanAccessOwnNotifications:
        return CanAccessOwnNotifications()

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        assert self._perm().has_permission(request, None) is False

    def test_authenticated_allowed(self) -> None:
        user = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = user
        assert self._perm().has_permission(request, None) is True

    def test_object_own_notification_allowed(self) -> None:
        user = UserFactory(role=UserRole.STUDENT)
        notification = Notification.objects.create(recipient=user, title="Test", message="Hello")
        request = factory.get("/")
        request.user = user
        assert self._perm().has_object_permission(request, None, notification) is True

    def test_object_other_notification_denied(self) -> None:
        owner = UserFactory(role=UserRole.STUDENT)
        other = UserFactory(role=UserRole.STUDENT)
        notification = Notification.objects.create(recipient=owner, title="Test", message="Hello")
        request = factory.get("/")
        request.user = other
        assert self._perm().has_object_permission(request, None, notification) is False
