"""Offer services."""

from django.core.exceptions import ValidationError

from apps.offers.models import Offer


def create_offer(*, company, title: str, description: str, **extra) -> Offer:
    if not company.is_active:
        raise ValidationError("Cannot create offers for an inactive company.")
    return Offer.objects.create(company=company, title=title, description=description, **extra)
