"""Company serializers."""

from rest_framework import serializers

from apps.companies.models import Company, CompanyMembership


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "description",
            "website",
            "city",
            "country",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CompanyMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMembership
        fields = ["id", "company", "user", "title", "is_owner", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
