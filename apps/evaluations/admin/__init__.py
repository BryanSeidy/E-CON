"""Evaluation admin."""

from django.contrib import admin

from apps.evaluations.models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("internship", "evaluator", "evaluation_type", "score", "submitted_at")
    list_filter = ("evaluation_type", "score", "is_deleted")
    search_fields = ("evaluator__email", "comment")
