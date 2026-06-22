"""Offer viewsets."""

from drf_spectacular.utils import extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from apps.offers.api.serializers import OfferSerializer
from apps.offers.models import Offer
from apps.offers.permissions import IsOfferReaderOrCompanyMember


@extend_schema(tags=["offers"])
class OfferViewSet(ModelViewSet):
    queryset = Offer.objects.none()
    serializer_class = OfferSerializer
    permission_classes = [IsOfferReaderOrCompanyMember]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description", "required_skills", "company__name", "location"]
    ordering_fields = ["created_at", "start_date", "end_date", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Offer.objects.select_related("company")
        if self.request.user.role == "COMPANY_MEMBER":
            queryset = queryset.filter(company__memberships__user=self.request.user).distinct()
        company_id = self.request.query_params.get("company")
        is_active = self.request.query_params.get("is_active")
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if is_active in {"true", "false"}:
            queryset = queryset.filter(is_active=is_active == "true")
        return queryset

    def perform_create(self, serializer):
        company = serializer.validated_data["company"]
        if (
            self.request.user.role != "SUPER_ADMIN"
            and not company.memberships.filter(user=self.request.user).exists()
        ):
            self.permission_denied(self.request, message="Cannot create offers for this company.")
        serializer.save()
