"""Tests for account models."""

from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.factories import StaffProfileFactory, StudentProfileFactory, UserFactory
from apps.accounts.models import StaffProfile, StudentProfile
from apps.common.models import UserRole

pytestmark = pytest.mark.django_db


def test_user_authenticates_with_email_and_uuid_primary_key() -> None:
    user = UserFactory(email="student@example.com", role=UserRole.STUDENT)

    assert user.email == "student@example.com"
    assert user.USERNAME_FIELD == "email"
    assert user.id.version == 4
    assert user.check_password("password")


def test_user_manager_creates_superuser() -> None:
    user_model = get_user_model()

    user = user_model.objects.create_superuser(email="admin@example.com", password="secret")

    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.role == UserRole.SUPER_ADMIN


def test_soft_deleted_users_are_hidden_by_default_manager() -> None:
    user = UserFactory()

    user.soft_delete(deleted_by=None)

    assert get_user_model().objects.filter(id=user.id).exists() is False
    assert get_user_model().all_objects.filter(id=user.id).exists() is True


def test_student_profile_fields() -> None:
    profile = StudentProfileFactory(student_number="S-001")

    assert profile.student_number == "S-001"
    assert profile.user.role == UserRole.STUDENT
    assert StudentProfile.objects.filter(id=profile.id).exists() is True


def test_staff_profile_fields() -> None:
    profile = StaffProfileFactory(role_scope="Programme")

    assert profile.role_scope == "Programme"
    assert profile.user.role == UserRole.ACADEMIC_SUPERVISOR
    assert StaffProfile.objects.filter(id=profile.id).exists() is True
