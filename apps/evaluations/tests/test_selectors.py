"""Tests for evaluation selectors."""

from __future__ import annotations

import uuid

import pytest

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import EvaluationType, InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.evaluations.models import Evaluation
from apps.evaluations.selectors import evaluation_list_for_user
from apps.internships.models import Internship
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db


def _setup():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    admin = UserFactory(role=UserRole.SUPER_ADMIN)
    company = Company.objects.create(name=f"EvalSel-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="Eval Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    internship = Internship.objects.create(
        application=application,
        offer=offer,
        student=student,
        company=company,
        academic_supervisor=supervisor,
        status=InternshipStatus.ACTIVE,
    )
    evaluation = Evaluation.objects.create(
        internship=internship,
        evaluator=supervisor,
        evaluation_type=EvaluationType.ACADEMIC,
        score=85,
    )
    return student, supervisor, company_user, admin, evaluation


class TestEvaluationListForUser:
    def test_company_member_sees_own_company_evaluations(self) -> None:
        _student, _sup, company_user, _admin, evaluation = _setup()
        qs = evaluation_list_for_user(company_user)
        assert evaluation.id in qs.values_list("id", flat=True)

    def test_supervisor_sees_supervised_evaluations(self) -> None:
        _student, supervisor, _co, _admin, evaluation = _setup()
        qs = evaluation_list_for_user(supervisor)
        assert evaluation.id in qs.values_list("id", flat=True)

    def test_admin_sees_all_evaluations(self) -> None:
        _student, _sup, _co, admin, evaluation = _setup()
        qs = evaluation_list_for_user(admin)
        assert evaluation.id in qs.values_list("id", flat=True)
