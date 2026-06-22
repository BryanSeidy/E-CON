"""Tests for evaluation permissions."""

from __future__ import annotations

import uuid
from unittest.mock import Mock

import pytest
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import EvaluationType, InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.evaluations.models import Evaluation
from apps.evaluations.permissions import CanManageEvaluations
from apps.internships.models import Internship
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


def _make_evaluation():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    company = Company.objects.create(name=f"EvalPerm-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="Perm Offer", description="D")
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
        score=75,
    )
    return student, supervisor, company_user, evaluation


class TestCanManageEvaluations:
    def _perm(self) -> CanManageEvaluations:
        return CanManageEvaluations()

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is False

    def test_student_read_allowed(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = student
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is True

    def test_student_write_denied(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.post("/")
        request.user = student
        view = Mock(action="create")
        assert self._perm().has_permission(request, view) is False

    def test_supervisor_write_allowed(self) -> None:
        supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
        request = factory.post("/")
        request.user = supervisor
        view = Mock(action="create")
        assert self._perm().has_permission(request, view) is True

    def test_object_student_read_own_internship(self) -> None:
        student, _sup, _co, evaluation = _make_evaluation()
        request = factory.get("/")
        request.user = student
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, evaluation) is True

    def test_object_student_write_denied(self) -> None:
        student, _sup, _co, evaluation = _make_evaluation()
        request = factory.put("/")
        request.user = student
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, evaluation) is False

    def test_object_supervisor_allowed(self) -> None:
        _student, supervisor, _co, evaluation = _make_evaluation()
        request = factory.put("/")
        request.user = supervisor
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, evaluation) is True

    def test_object_company_member_allowed(self) -> None:
        _student, _sup, company_user, evaluation = _make_evaluation()
        request = factory.get("/")
        request.user = company_user
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, evaluation) is True

    def test_object_super_admin_allowed(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        _student, _sup, _co, evaluation = _make_evaluation()
        request = factory.put("/")
        request.user = admin
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, evaluation) is True

    def test_object_unrelated_student_denied(self) -> None:
        _student, _sup, _co, evaluation = _make_evaluation()
        other_student = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = other_student
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, evaluation) is False
