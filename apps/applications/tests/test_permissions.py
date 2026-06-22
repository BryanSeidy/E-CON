"""Tests for application permissions."""

from __future__ import annotations

import uuid
from unittest.mock import Mock

import pytest
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.applications.permissions import CanManageApplications
from apps.common.models import UserRole
from apps.companies.models import Company, CompanyMembership
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


def _make_application():
    student = UserFactory(role=UserRole.STUDENT)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    company = Company.objects.create(name=f"AppPerm-{uuid.uuid4().hex[:8]}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="AppPerm Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    return student, company_user, application


class TestCanManageApplications:
    def _perm(self) -> CanManageApplications:
        return CanManageApplications()

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is False

    def test_create_allowed_for_student(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.post("/")
        request.user = student
        view = Mock(action="create")
        assert self._perm().has_permission(request, view) is True

    def test_create_denied_for_non_student(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.post("/")
        request.user = member
        view = Mock(action="create")
        assert self._perm().has_permission(request, view) is False

    def test_list_allowed_for_student(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = student
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is True

    def test_list_allowed_for_company_member(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.get("/")
        request.user = member
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is True

    def test_list_denied_for_supervisor(self) -> None:
        sup = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
        request = factory.get("/")
        request.user = sup
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is False

    def test_object_student_read_own(self) -> None:
        student, _co, application = _make_application()
        request = factory.get("/")
        request.user = student
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, application) is True

    def test_object_student_write_denied(self) -> None:
        student, _co, application = _make_application()
        request = factory.put("/")
        request.user = student
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, application) is False

    def test_object_company_member_allowed(self) -> None:
        _stu, company_user, application = _make_application()
        request = factory.get("/")
        request.user = company_user
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, application) is True

    def test_object_super_admin_allowed(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        _stu, _co, application = _make_application()
        request = factory.put("/")
        request.user = admin
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, application) is True

    def test_object_unrelated_student_denied(self) -> None:
        _stu, _co, application = _make_application()
        other = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = other
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, application) is False
