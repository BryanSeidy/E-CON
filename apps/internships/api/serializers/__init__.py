"""Internship serializers."""

from rest_framework import serializers

from apps.internships.models import Internship


class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = [
            "id",
            "application",
            "offer",
            "student",
            "company",
            "academic_supervisor",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "application",
            "offer",
            "student",
            "company",
            "created_at",
            "updated_at",
        ]
