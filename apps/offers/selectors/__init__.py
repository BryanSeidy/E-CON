"""Offer selectors."""

from apps.offers.models import Offer


def active_offer_list():
    return Offer.objects.filter(is_active=True).select_related("company")
