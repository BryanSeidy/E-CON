"""Evaluation serializers."""

from rest_framework import serializers

from apps.evaluations.models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = [
            "id",
            "internship",
            "evaluator",
            "evaluation_type",
            "score",
            "comment",
            "submitted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "evaluator", "submitted_at", "created_at", "updated_at"]
