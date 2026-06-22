"""Offer serializers."""

from rest_framework import serializers

from apps.offers.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            "id",
            "company",
            "title",
            "description",
            "location",
            "required_skills",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
