"""Tests for offer services."""

from __future__ import annotations

import uuid

import pytest

from apps.companies.models import Company
from apps.offers.models import Offer
from apps.offers.services import create_offer

pytestmark = pytest.mark.django_db


class TestCreateOffer:
    def test_creates_offer(self) -> None:
        company = Company.objects.create(name=f"OfferCo-{uuid.uuid4().hex[:8]}")
        offer = create_offer(company=company, title="Dev Intern", description="Build things")

        assert offer.title == "Dev Intern"
        assert offer.company == company
        assert Offer.objects.filter(id=offer.id).exists()

    def test_creates_offer_with_extra_fields(self) -> None:
        company = Company.objects.create(name=f"ExtraCo-{uuid.uuid4().hex[:8]}")
        offer = create_offer(
            company=company,
            title="Offer",
            description="Desc",
            location="Paris",
            required_skills="Python",
        )
        assert offer.location == "Paris"
        assert offer.required_skills == "Python"
