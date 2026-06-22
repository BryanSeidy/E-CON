"""Tests for common querysets and managers."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestSoftDeleteQuerySet:
    def test_alive_excludes_deleted_rows(self) -> None:
        user = UserFactory()
        user.soft_delete()

        assert User.objects.filter(id=user.id).exists() is False

    def test_deleted_returns_only_deleted_rows(self) -> None:
        active = UserFactory()
        deleted = UserFactory()
        deleted.soft_delete()

        qs = User.all_objects.all().deleted()
        assert deleted.id in qs.values_list("id", flat=True)
        assert active.id not in qs.values_list("id", flat=True)

    def test_queryset_soft_delete_marks_rows(self) -> None:
        u1 = UserFactory()
        u2 = UserFactory()

        count = User.all_objects.filter(id__in=[u1.id, u2.id]).soft_delete()

        assert count == 2
        u1.refresh_from_db()
        u2.refresh_from_db()
        assert u1.is_deleted is True
        assert u1.deleted_at is not None
        assert u2.is_deleted is True

    def test_queryset_restore_clears_deletion(self) -> None:
        u1 = UserFactory()
        u1.soft_delete()

        count = User.all_objects.filter(id=u1.id).restore()

        assert count == 1
        u1.refresh_from_db()
        assert u1.is_deleted is False
        assert u1.deleted_at is None
        assert u1.deleted_by is None


class TestSoftDeleteModel:
    def test_soft_delete_sets_fields(self) -> None:
        user = UserFactory()
        deleter = UserFactory(role=UserRole.SUPER_ADMIN)

        user.soft_delete(deleted_by=deleter)

        user.refresh_from_db()
        assert user.is_deleted is True
        assert user.deleted_at is not None
        assert user.deleted_by_id == deleter.id

    def test_soft_delete_without_save(self) -> None:
        user = UserFactory()

        user.soft_delete(save=False)

        assert user.is_deleted is True
        user.refresh_from_db()
        assert user.is_deleted is False

    def test_restore_clears_fields(self) -> None:
        user = UserFactory()
        user.soft_delete()
        user.refresh_from_db()

        user.restore()

        user.refresh_from_db()
        assert user.is_deleted is False
        assert user.deleted_at is None
        assert user.deleted_by is None

    def test_restore_without_save(self) -> None:
        user = UserFactory()
        user.soft_delete()
        user.refresh_from_db()

        user.restore(save=False)

        assert user.is_deleted is False
        user.refresh_from_db()
        assert user.is_deleted is True


class TestSoftDeleteManager:
    def test_default_manager_hides_deleted(self) -> None:
        user = UserFactory()
        user.soft_delete()

        assert User.objects.filter(id=user.id).count() == 0

    def test_all_objects_manager_shows_deleted(self) -> None:
        user = UserFactory()
        user.soft_delete()

        assert User.all_objects.filter(id=user.id).count() == 1
