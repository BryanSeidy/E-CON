"""Tests for application selectors."""

from __future__ import annotations

import uuid

import pytest

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.applications.selectors import application_list_for_user
from apps.common.models import UserRole
from apps.companies.models import Company, CompanyMembership
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db


def _setup():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    admin = UserFactory(role=UserRole.SUPER_ADMIN)
    company = Company.objects.create(name=f"AppSel-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="AppSel Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    return student, company_user, admin, application


class TestApplicationListForUser:
    def test_student_sees_own_applications(self) -> None:
        student, _co, _admin, application = _setup()
        qs = application_list_for_user(student)
        assert application.id in qs.values_list("id", flat=True)

    def test_company_member_sees_company_applications(self) -> None:
        _stu, company_user, _admin, application = _setup()
        qs = application_list_for_user(company_user)
        assert application.id in qs.values_list("id", flat=True)

    def test_admin_sees_all_applications(self) -> None:
        _stu, _co, admin, application = _setup()
        qs = application_list_for_user(admin)
        assert application.id in qs.values_list("id", flat=True)

    def test_unrelated_student_sees_nothing(self) -> None:
        _setup()
        other = UserFactory(role=UserRole.STUDENT)
        qs = application_list_for_user(other)
        assert qs.count() == 0
