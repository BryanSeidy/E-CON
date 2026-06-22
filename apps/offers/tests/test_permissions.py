"""Tests for offer permissions."""

from __future__ import annotations

import uuid

import pytest
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole
from apps.companies.models import Company, CompanyMembership
from apps.offers.models import Offer
from apps.offers.permissions import IsOfferReaderOrCompanyMember

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


def _co(name: str = "Co") -> Company:
    return Company.objects.create(name=f"{name}-{uuid.uuid4().hex[:8]}")


class TestIsOfferReaderOrCompanyMember:
    def _perm(self) -> IsOfferReaderOrCompanyMember:
        return IsOfferReaderOrCompanyMember()

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        assert self._perm().has_permission(request, None) is False

    def test_safe_method_allowed(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.get("/")
        request.user = student
        assert self._perm().has_permission(request, None) is True

    def test_write_denied_for_non_company(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.post("/")
        request.user = student
        assert self._perm().has_permission(request, None) is False

    def test_write_allowed_for_company_member(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.post("/")
        request.user = member
        assert self._perm().has_permission(request, None) is True

    def test_write_allowed_for_super_admin(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        request = factory.post("/")
        request.user = admin
        assert self._perm().has_permission(request, None) is True

    def test_object_safe_method_allowed(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        company = _co("OfferPerm")
        offer = Offer.objects.create(company=company, title="Offer", description="D")
        request = factory.get("/")
        request.user = student
        assert self._perm().has_object_permission(request, None, offer) is True

    def test_object_write_super_admin_allowed(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        company = _co("OfferAdmin")
        offer = Offer.objects.create(company=company, title="Admin Offer", description="D")
        request = factory.put("/")
        request.user = admin
        assert self._perm().has_object_permission(request, None, offer) is True

    def test_object_write_member_allowed(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        company = _co("OfferMem")
        CompanyMembership.objects.create(company=company, user=member)
        offer = Offer.objects.create(company=company, title="Member Offer", description="D")
        request = factory.put("/")
        request.user = member
        assert self._perm().has_object_permission(request, None, offer) is True

    def test_object_write_non_member_denied(self) -> None:
        member = UserFactory(role=UserRole.COMPANY_MEMBER)
        company = _co("OfferNon")
        offer = Offer.objects.create(company=company, title="Non Offer", description="D")
        request = factory.put("/")
        request.user = member
        assert self._perm().has_object_permission(request, None, offer) is False
