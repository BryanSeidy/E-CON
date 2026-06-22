"""Evaluation domain models."""

from __future__ import annotations

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import BaseSoftDeleteModel, EvaluationType


class Evaluation(BaseSoftDeleteModel):
    internship = models.ForeignKey(
        "internships.Internship", on_delete=models.CASCADE, related_name="evaluations"
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="given_evaluations"
    )
    evaluation_type = models.CharField(max_length=20, choices=EvaluationType.choices)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["internship", "evaluation_type"],
                name="unique_evaluation_type_per_internship",
            )
        ]

    def __str__(self) -> str:
        return f"{self.internship} - {self.evaluation_type}"
