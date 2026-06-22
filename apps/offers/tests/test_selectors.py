"""Tests for offer selectors."""

from __future__ import annotations

import uuid

import pytest

from apps.companies.models import Company
from apps.offers.models import Offer
from apps.offers.selectors import active_offer_list

pytestmark = pytest.mark.django_db


class TestActiveOfferList:
    def test_returns_only_active_offers(self) -> None:
        uid = uuid.uuid4().hex[:8]
        company = Company.objects.create(name=f"SelCo-{uid}")
        Offer.objects.create(company=company, title="Active", description="Yes", is_active=True)
        Offer.objects.create(company=company, title="Inactive", description="No", is_active=False)

        qs = active_offer_list()
        titles = list(qs.values_list("title", flat=True))
        assert "Active" in titles
        assert "Inactive" not in titles
