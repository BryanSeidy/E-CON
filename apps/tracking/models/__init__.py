"""Tracking domain models."""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.common.models import BaseSoftDeleteModel


class WeeklyLog(BaseSoftDeleteModel):
    internship = models.ForeignKey(
        "internships.Internship", on_delete=models.CASCADE, related_name="weekly_logs"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weekly_logs"
    )
    week_start = models.DateField()
    activities = models.TextField()
    blockers = models.TextField(blank=True)
    next_steps = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-week_start"]
        constraints = [
            models.UniqueConstraint(
                fields=["internship", "week_start"], name="unique_weekly_log_per_internship_week"
            )
        ]

    def __str__(self) -> str:
        return f"{self.internship} - {self.week_start}"
