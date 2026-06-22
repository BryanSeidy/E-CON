"""AI matching serializers."""

from rest_framework import serializers


class OfferMatchSerializer(serializers.Serializer):
    offer = serializers.IntegerField()
    title = serializers.CharField()
    company = serializers.IntegerField()
    company_name = serializers.CharField()
    location = serializers.CharField(allow_blank=True)
    score = serializers.FloatField()
    matched_skills = serializers.ListField(child=serializers.CharField())
