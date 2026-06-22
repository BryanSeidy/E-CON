"""Tests for internship services edge cases."""

from __future__ import annotations

import uuid

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import InternshipStatus, UserRole
from apps.companies.models import Company
from apps.internships.services import (
    assign_academic_supervisor,
    complete_internship,
    create_internship_from_application,
)
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db


def _make_application():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    company = Company.objects.create(name=f"IntSvc-{uid}")
    offer = Offer.objects.create(company=company, title="Svc Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    return application, student, company


class TestCreateInternshipFromApplication:
    def test_creates_internship(self) -> None:
        application, student, company = _make_application()
        internship = create_internship_from_application(application=application)

        assert internship.student == student
        assert internship.company == company
        assert internship.status == InternshipStatus.ASSIGNED

    def test_idempotent_does_not_duplicate(self) -> None:
        application, _stu, _co = _make_application()
        first = create_internship_from_application(application=application)
        second = create_internship_from_application(application=application)
        assert first.id == second.id


class TestAssignAcademicSupervisor:
    def test_assigns_supervisor(self) -> None:
        application, _stu, _co = _make_application()
        internship = create_internship_from_application(application=application)
        supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)

        result = assign_academic_supervisor(internship=internship, supervisor=supervisor)

        assert result.academic_supervisor == supervisor
        assert result.status == InternshipStatus.ACTIVE

    def test_rejects_completed_internship(self) -> None:
        application, _stu, _co = _make_application()
        internship = create_internship_from_application(application=application)
        internship.status = InternshipStatus.COMPLETED
        internship.save(update_fields=["status"])

        with pytest.raises(ValidationError):
            assign_academic_supervisor(internship=internship, supervisor=None)


class TestCompleteInternship:
    def test_completes_active_internship(self) -> None:
        application, _stu, _co = _make_application()
        internship = create_internship_from_application(application=application)
        internship.status = InternshipStatus.ACTIVE
        internship.save(update_fields=["status"])

        result = complete_internship(internship=internship)
        assert result.status == InternshipStatus.COMPLETED

    def test_rejects_non_active_internship(self) -> None:
        application, _stu, _co = _make_application()
        internship = create_internship_from_application(application=application)

        with pytest.raises(ValidationError):
            complete_internship(internship=internship)
