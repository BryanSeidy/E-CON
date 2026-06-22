"""Tests for company services."""

from __future__ import annotations

import pytest

from apps.accounts.factories import UserFactory
from apps.common.models import UserRole
from apps.companies.models import Company, CompanyMembership
from apps.companies.services import add_company_member, create_company

pytestmark = pytest.mark.django_db


class TestCreateCompany:
    def test_creates_company_with_required_fields(self) -> None:
        company = create_company(name="Acme Corp")
        assert company.name == "Acme Corp"
        assert Company.objects.filter(id=company.id).exists()

    def test_creates_company_with_optional_fields(self) -> None:
        company = create_company(
            name="Startup", description="A startup", website="https://startup.io"
        )
        assert company.description == "A startup"
        assert company.website == "https://startup.io"


class TestAddCompanyMember:
    def test_adds_member_to_company(self) -> None:
        company = create_company(name="Acme")
        user = UserFactory(role=UserRole.COMPANY_MEMBER)
        membership = add_company_member(company=company, user=user)

        assert isinstance(membership, CompanyMembership)
        assert membership.company == company
        assert membership.user == user
        assert membership.is_owner is False

    def test_adds_owner_member(self) -> None:
        company = create_company(name="OwnerCo")
        user = UserFactory(role=UserRole.COMPANY_MEMBER)
        membership = add_company_member(company=company, user=user, title="CEO", is_owner=True)

        assert membership.is_owner is True
        assert membership.title == "CEO"
