"""Audit serializers."""

from rest_framework import serializers


class AuditContextSerializer(serializers.Serializer):
    actor_id = serializers.IntegerField()
    actor_email = serializers.EmailField()
    actor_role = serializers.CharField()
    source = serializers.CharField()
    tenant = serializers.DictField(child=serializers.CharField(allow_blank=True), required=False)
