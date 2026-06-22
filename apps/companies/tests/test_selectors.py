"""Tests for company selectors."""

from __future__ import annotations

import uuid

import pytest

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole
from apps.companies.models import Company, CompanyMembership
from apps.companies.selectors import company_list, memberships_for_user

pytestmark = pytest.mark.django_db


class TestCompanyList:
    def test_returns_active_companies(self) -> None:
        uid = uuid.uuid4().hex[:8]
        Company.objects.create(name=f"Active-{uid}", is_active=True)
        Company.objects.create(name=f"Inactive-{uid}", is_active=False)

        qs = company_list()
        names = list(qs.values_list("name", flat=True))
        assert f"Active-{uid}" in names
        assert f"Inactive-{uid}" not in names


class TestMembershipsForUser:
    def test_returns_memberships_for_given_user(self) -> None:
        uid = uuid.uuid4().hex[:8]
        user = UserFactory(role=UserRole.COMPANY_MEMBER)
        other = UserFactory(role=UserRole.COMPANY_MEMBER)
        company = Company.objects.create(name=f"TestCo-{uid}")
        CompanyMembership.objects.create(company=company, user=user)
        CompanyMembership.objects.create(company=company, user=other)

        qs = memberships_for_user(user)
        assert qs.count() == 1
        assert qs.first().user == user
