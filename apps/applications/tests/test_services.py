"""Tests for application services."""

from __future__ import annotations

import uuid

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.factories import UserFactory
from apps.applications.services import reject_application, submit_application
from apps.common.models import ApplicationStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db


def _setup():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    company = Company.objects.create(name=f"AppSvc-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="AppSvc Offer", description="D")
    return student, company_user, offer


class TestSubmitApplication:
    def test_inactive_offer_raises(self) -> None:
        student, _co, offer = _setup()
        offer.is_active = False
        offer.save(update_fields=["is_active"])

        with pytest.raises(ValidationError, match="inactive"):
            submit_application(offer=offer, student=student)

    def test_duplicate_submit_is_idempotent(self) -> None:
        student, _co, offer = _setup()
        first = submit_application(offer=offer, student=student, cover_letter="Hello")
        second = submit_application(offer=offer, student=student)
        assert first.id == second.id

    def test_cannot_update_after_review(self) -> None:
        student, _co, offer = _setup()
        app = submit_application(offer=offer, student=student)
        app.status = ApplicationStatus.ACCEPTED
        app.save(update_fields=["status"])

        with pytest.raises(ValidationError, match="after review"):
            submit_application(offer=offer, student=student)


class TestRejectApplication:
    def test_rejects_pending_application(self) -> None:
        student, company_user, offer = _setup()
        app = submit_application(offer=offer, student=student)

        result = reject_application(application=app, reviewed_by=company_user)

        assert result.status == ApplicationStatus.REJECTED
        assert result.reviewed_by == company_user
        assert result.reviewed_at is not None

    def test_rejects_non_pending_raises(self) -> None:
        student, company_user, offer = _setup()
        app = submit_application(offer=offer, student=student)
        app.status = ApplicationStatus.ACCEPTED
        app.save(update_fields=["status"])

        with pytest.raises(ValidationError):
            reject_application(application=app, reviewed_by=company_user)
