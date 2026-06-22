"""Tests for tracking permissions."""

from __future__ import annotations

import uuid
from unittest.mock import Mock

import pytest
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.internships.models import Internship
from apps.offers.models import Offer
from apps.tracking.models import WeeklyLog
from apps.tracking.permissions import CanAccessWeeklyLogs

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


def _make_log():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    company = Company.objects.create(name=f"TrkPerm-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="TrkPerm Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    internship = Internship.objects.create(
        application=application,
        offer=offer,
        student=student,
        company=company,
        academic_supervisor=supervisor,
        status=InternshipStatus.ACTIVE,
    )
    log = WeeklyLog.objects.create(
        internship=internship,
        student=student,
        week_start=timezone.now().date(),
        activities="Testing",
        submitted_at=timezone.now(),
    )
    return student, supervisor, company_user, log


class TestCanAccessWeeklyLogs:
    def _perm(self) -> CanAccessWeeklyLogs:
        return CanAccessWeeklyLogs()

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

    def test_list_allowed_for_any_authenticated(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.get("/")
        request.user = member
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is True

    def test_object_student_own_allowed(self) -> None:
        student, _sup, _co, log = _make_log()
        request = factory.get("/")
        request.user = student
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, log) is True

    def test_object_super_admin_allowed(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        _stu, _sup, _co, log = _make_log()
        request = factory.put("/")
        request.user = admin
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, log) is True

    def test_object_company_member_read_allowed(self) -> None:
        _stu, _sup, company_user, log = _make_log()
        request = factory.get("/")
        request.user = company_user
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, log) is True

    def test_object_company_member_write_denied(self) -> None:
        _stu, _sup, company_user, log = _make_log()
        request = factory.put("/")
        request.user = company_user
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, log) is False

    def test_object_supervisor_read_allowed(self) -> None:
        _stu, supervisor, _co, log = _make_log()
        request = factory.get("/")
        request.user = supervisor
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, log) is True

    def test_object_supervisor_write_denied(self) -> None:
        _stu, supervisor, _co, log = _make_log()
        request = factory.put("/")
        request.user = supervisor
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, log) is False

    def test_object_unrelated_student_denied(self) -> None:
        _stu, _sup, _co, log = _make_log()
        other = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = other
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, log) is False
