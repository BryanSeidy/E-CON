"""Offer viewsets."""

from rest_framework.viewsets import ModelViewSet

from apps.offers.api.serializers import OfferSerializer
from apps.offers.models import Offer
from apps.offers.permissions import IsOfferReaderOrCompanyMember


class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.select_related("company")
    serializer_class = OfferSerializer
    permission_classes = [IsOfferReaderOrCompanyMember]
