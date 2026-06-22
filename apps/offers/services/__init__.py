"""Offer services."""

from apps.offers.models import Offer


def create_offer(*, company, title: str, description: str, **extra) -> Offer:
    return Offer.objects.create(company=company, title=title, description=description, **extra)
