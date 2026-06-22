"""Tests for internship permissions."""

from __future__ import annotations

import uuid
from unittest.mock import Mock

import pytest
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.internships.models import Internship
from apps.internships.permissions import CanAccessInternships
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


def _make_internship():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    company = Company.objects.create(name=f"IntPerm-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="Int Perm Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    internship = Internship.objects.create(
        application=application,
        offer=offer,
        student=student,
        company=company,
        academic_supervisor=supervisor,
        status=InternshipStatus.ACTIVE,
    )
    return student, supervisor, company_user, internship


class TestCanAccessInternships:
    def _perm(self) -> CanAccessInternships:
        return CanAccessInternships()

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is False

    def test_student_allowed(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = student
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is True

    def test_object_student_read_own(self) -> None:
        student, _sup, _co, internship = _make_internship()
        request = factory.get("/")
        request.user = student
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, internship) is True

    def test_object_student_write_denied(self) -> None:
        student, _sup, _co, internship = _make_internship()
        request = factory.put("/")
        request.user = student
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, internship) is False

    def test_object_supervisor_allowed(self) -> None:
        _stu, supervisor, _co, internship = _make_internship()
        request = factory.get("/")
        request.user = supervisor
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, internship) is True

    def test_object_company_member_allowed(self) -> None:
        _stu, _sup, company_user, internship = _make_internship()
        request = factory.get("/")
        request.user = company_user
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, internship) is True

    def test_object_super_admin_allowed(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        _stu, _sup, _co, internship = _make_internship()
        request = factory.put("/")
        request.user = admin
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, internship) is True

    def test_object_unrelated_supervisor_denied(self) -> None:
        _stu, _sup, _co, internship = _make_internship()
        other_sup = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
        request = factory.get("/")
        request.user = other_sup
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, internship) is False

    def test_object_unrelated_company_member_denied(self) -> None:
        _stu, _sup, _co, internship = _make_internship()
        other_co = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.get("/")
        request.user = other_co
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, internship) is False
