"""Institution serializers."""

from rest_framework import serializers

from apps.institutions.models import Department, Institution


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "name", "code", "country", "city", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "institution", "name", "code", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
