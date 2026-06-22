"""Tests for company permissions."""

from __future__ import annotations

import uuid

import pytest
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole
from apps.companies.models import Company, CompanyMembership
from apps.companies.permissions import IsCompanyMemberOrAdmin

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


class TestIsCompanyMemberOrAdmin:
    def _perm(self) -> IsCompanyMemberOrAdmin:
        return IsCompanyMemberOrAdmin()

    def _co(self, name: str = "Co") -> Company:
        return Company.objects.create(name=f"{name}-{uuid.uuid4().hex[:8]}")

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        assert self._perm().has_permission(request, None) is False

    def test_safe_methods_allowed_for_any_authenticated_user(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = student
        assert self._perm().has_permission(request, None) is True

    def test_write_denied_for_non_company_roles(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.post("/")
        request.user = student
        assert self._perm().has_permission(request, None) is False

    def test_write_allowed_for_company_member(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.post("/")
        request.user = member
        assert self._perm().has_permission(request, None) is True

    def test_write_allowed_for_super_admin(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        request = factory.post("/")
        request.user = admin
        assert self._perm().has_permission(request, None) is True

    def test_object_safe_method_allowed(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        company = self._co("ObjPerm")
        request = factory.get("/")
        request.user = student
        assert self._perm().has_object_permission(request, None, company) is True

    def test_object_write_allowed_for_super_admin(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        company = self._co("Admin")
        request = factory.put("/")
        request.user = admin
        assert self._perm().has_object_permission(request, None, company) is True

    def test_object_write_allowed_for_own_company_member(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        company = self._co("My")
        CompanyMembership.objects.create(company=company, user=member)
        request = factory.put("/")
        request.user = member
        assert self._perm().has_object_permission(request, None, company) is True

    def test_object_write_denied_for_non_member(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        company = self._co("NotMy")
        request = factory.put("/")
        request.user = member
        assert self._perm().has_object_permission(request, None, company) is False
