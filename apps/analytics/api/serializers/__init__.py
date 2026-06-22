"""Analytics serializers."""

from rest_framework import serializers


class AnalyticsSummarySerializer(serializers.Serializer):
    offers = serializers.IntegerField()
    applications = serializers.IntegerField()
    internships = serializers.IntegerField()
    documents = serializers.IntegerField()
    notifications = serializers.IntegerField()
