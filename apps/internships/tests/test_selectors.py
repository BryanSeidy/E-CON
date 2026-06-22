"""Tests for internship selectors."""

from __future__ import annotations

import uuid

import pytest

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.internships.models import Internship
from apps.internships.selectors import internship_list_for_user
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db


def _setup():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    admin = UserFactory(role=UserRole.SUPER_ADMIN)
    company = Company.objects.create(name=f"IntSel-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="Int Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    internship = Internship.objects.create(
        application=application,
        offer=offer,
        student=student,
        company=company,
        academic_supervisor=supervisor,
        status=InternshipStatus.ACTIVE,
    )
    return student, supervisor, company_user, admin, internship


class TestInternshipListForUser:
    def test_student_sees_own_internships(self) -> None:
        student, _sup, _co, _admin, internship = _setup()
        qs = internship_list_for_user(student)
        assert internship.id in qs.values_list("id", flat=True)

    def test_supervisor_sees_supervised_internships(self) -> None:
        _stu, supervisor, _co, _admin, internship = _setup()
        qs = internship_list_for_user(supervisor)
        assert internship.id in qs.values_list("id", flat=True)

    def test_company_member_sees_company_internships(self) -> None:
        _stu, _sup, company_user, _admin, internship = _setup()
        qs = internship_list_for_user(company_user)
        assert internship.id in qs.values_list("id", flat=True)

    def test_admin_sees_all_internships(self) -> None:
        _stu, _sup, _co, admin, internship = _setup()
        qs = internship_list_for_user(admin)
        assert internship.id in qs.values_list("id", flat=True)

    def test_unrelated_student_sees_nothing(self) -> None:
        _setup()
        other = UserFactory(role=UserRole.STUDENT)
        qs = internship_list_for_user(other)
        assert qs.count() == 0
