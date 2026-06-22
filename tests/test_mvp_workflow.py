"""Minimum MVP workflow tests."""

from __future__ import annotations

import pytest
from apps.applications.services import accept_application, submit_application
from apps.common.models import EvaluationType, InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.documents.services import submit_document
from apps.evaluations.services import submit_evaluation
from apps.institutions.models import Department, Institution
from apps.internships.services import assign_academic_supervisor, complete_internship
from apps.notifications.services import mark_as_read, notify
from apps.offers.models import Offer
from apps.tracking.services import submit_weekly_log
from django.contrib.auth import get_user_model
from django.utils import timezone

pytestmark = pytest.mark.django_db


def test_student_to_completed_internship_workflow() -> None:
    user_model = get_user_model()
    student = user_model.objects.create_user(
        email="student@econ.test", password="pass", role=UserRole.STUDENT
    )
    company_user = user_model.objects.create_user(
        email="company@econ.test", password="pass", role=UserRole.COMPANY_MEMBER
    )
    supervisor = user_model.objects.create_user(
        email="supervisor@econ.test", password="pass", role=UserRole.ACADEMIC_SUPERVISOR
    )
    institution = Institution.objects.create(name="E-CON University", code="ECON")
    Department.objects.create(institution=institution, name="Computer Science", code="CS")
    company = Company.objects.create(name="Linear Labs")
    CompanyMembership.objects.create(company=company, user=company_user, is_owner=True)
    offer = Offer.objects.create(
        company=company, title="Backend Internship", description="Build MVP workflows"
    )

    application = submit_application(offer=offer, student=student, cover_letter="Ready")
    internship = accept_application(application=application, reviewed_by=company_user)
    internship = assign_academic_supervisor(internship=internship, supervisor=supervisor)
    document = submit_document(internship=internship, uploaded_by=student, title="Convention")
    log = submit_weekly_log(
        internship=internship,
        student=student,
        week_start=timezone.now().date(),
        activities="Delivery",
    )
    evaluation = submit_evaluation(
        internship=internship,
        evaluator=supervisor,
        evaluation_type=EvaluationType.ACADEMIC,
        score=91,
    )
    notification = mark_as_read(
        notification=notify(recipient=student, title="Stage", message="Terminé")
    )
    internship = complete_internship(internship=internship)

    assert internship.status == InternshipStatus.COMPLETED
    assert internship.academic_supervisor == supervisor
    assert document.uploaded_by == student
    assert log.submitted_at is not None
    assert evaluation.score == 91
    assert notification.is_read is True
