"""Tests for tracking selectors."""

from __future__ import annotations

import uuid

import pytest
from django.utils import timezone

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.internships.models import Internship
from apps.offers.models import Offer
from apps.tracking.models import WeeklyLog
from apps.tracking.selectors import weekly_log_list_for_user

pytestmark = pytest.mark.django_db


def _setup():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    admin = UserFactory(role=UserRole.SUPER_ADMIN)
    company = Company.objects.create(name=f"TrkSel-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="Trk Offer", description="D")
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
        activities="Built features",
        submitted_at=timezone.now(),
    )
    return student, supervisor, company_user, admin, log


class TestWeeklyLogListForUser:
    def test_student_sees_own_logs(self) -> None:
        student, _sup, _co, _admin, log = _setup()
        qs = weekly_log_list_for_user(student)
        assert log.id in qs.values_list("id", flat=True)

    def test_supervisor_sees_supervised_logs(self) -> None:
        _stu, supervisor, _co, _admin, log = _setup()
        qs = weekly_log_list_for_user(supervisor)
        assert log.id in qs.values_list("id", flat=True)

    def test_company_member_sees_company_logs(self) -> None:
        _stu, _sup, company_user, _admin, log = _setup()
        qs = weekly_log_list_for_user(company_user)
        assert log.id in qs.values_list("id", flat=True)

    def test_admin_sees_all_logs(self) -> None:
        _stu, _sup, _co, admin, log = _setup()
        qs = weekly_log_list_for_user(admin)
        assert log.id in qs.values_list("id", flat=True)
