"""Tests for common abstract base models."""

from __future__ import annotations

import uuid

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUUIDModel:
    def test_user_has_uuid4_primary_key(self) -> None:
        user = UserFactory()
        assert isinstance(user.id, uuid.UUID)
        assert user.id.version == 4


class TestTimestampedModel:
    def test_created_at_and_updated_at_are_set(self) -> None:
        user = UserFactory()
        assert user.created_at is not None
        assert user.updated_at is not None


class TestUserFullName:
    def test_full_name_returns_combined(self) -> None:
        user = UserFactory(first_name="Alice", last_name="Dupont")
        assert user.full_name == "Alice Dupont"

    def test_full_name_strips_whitespace(self) -> None:
        user = UserFactory(first_name="", last_name="")
        assert user.full_name == ""

    def test_full_name_with_only_first_name(self) -> None:
        user = UserFactory(first_name="Alice", last_name="")
        assert user.full_name == "Alice"


class TestUserStr:
    def test_str_returns_email(self) -> None:
        user = UserFactory(email="test@example.com")
        assert str(user) == "test@example.com"


class TestUserManagerEdgeCases:
    def test_create_user_without_email_raises(self) -> None:
        with pytest.raises(ValueError, match="email"):
            get_user_model().objects.create_user(email="", password="pass")

    def test_create_superuser_not_staff_raises(self) -> None:
        with pytest.raises(ValueError, match="is_staff"):
            get_user_model().objects.create_superuser(
                email="admin@example.com", password="pass", is_staff=False
            )

    def test_create_superuser_not_superuser_raises(self) -> None:
        with pytest.raises(ValueError, match="is_superuser"):
            get_user_model().objects.create_superuser(
                email="admin@example.com", password="pass", is_superuser=False
            )


class TestProfileStr:
    def test_student_profile_str(self) -> None:
        from apps.accounts.factories import StudentProfileFactory

        profile = StudentProfileFactory(student_number="STU-999")
        assert str(profile) == "STU-999"

    def test_staff_profile_str(self) -> None:
        from apps.accounts.factories import StaffProfileFactory

        profile = StaffProfileFactory(university="MIT", role_scope="Research")
        assert str(profile) == "MIT - Research"
