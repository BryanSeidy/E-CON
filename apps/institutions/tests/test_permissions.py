"""Tests for institution permissions."""

from __future__ import annotations

import uuid

import pytest
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole
from apps.institutions.models import Institution
from apps.institutions.permissions import IsInstitutionAdminOrReadOnly

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


def _inst(name: str = "Inst") -> Institution:
    uid = uuid.uuid4().hex[:8]
    return Institution.objects.create(name=f"{name}-{uid}", code=f"I{uid[:4]}")


class TestIsInstitutionAdminOrReadOnly:
    def _perm(self) -> IsInstitutionAdminOrReadOnly:
        return IsInstitutionAdminOrReadOnly()

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        assert self._perm().has_permission(request, None) is False

    def test_safe_method_allowed_for_any_authenticated(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = student
        assert self._perm().has_permission(request, None) is True

    def test_write_denied_for_non_admin(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.post("/")
        request.user = student
        assert self._perm().has_permission(request, None) is False

    def test_write_allowed_for_university_admin(self) -> None:
        admin = UserFactory(role=UserRole.UNIVERSITY_ADMIN)
        request = factory.post("/")
        request.user = admin
        assert self._perm().has_permission(request, None) is True

    def test_write_allowed_for_super_admin(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        request = factory.post("/")
        request.user = admin
        assert self._perm().has_permission(request, None) is True

    def test_object_safe_method_allowed(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        inst = _inst()
        request = factory.get("/")
        request.user = student
        assert self._perm().has_object_permission(request, None, inst) is True

    def test_object_write_allowed_for_university_admin(self) -> None:
        admin = UserFactory(role=UserRole.UNIVERSITY_ADMIN)
        inst = _inst()
        request = factory.put("/")
        request.user = admin
        assert self._perm().has_object_permission(request, None, inst) is True

    def test_object_write_denied_for_non_admin(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        inst = _inst()
        request = factory.put("/")
        request.user = student
        assert self._perm().has_object_permission(request, None, inst) is False
