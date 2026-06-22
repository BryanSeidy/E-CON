"""Tracking serializers."""

from rest_framework import serializers

from apps.tracking.models import WeeklyLog


class WeeklyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyLog
        fields = [
            "id",
            "internship",
            "student",
            "week_start",
            "activities",
            "blockers",
            "next_steps",
            "submitted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "student", "submitted_at", "created_at", "updated_at"]
