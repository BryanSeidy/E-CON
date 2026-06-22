"""Tracking admin."""

from django.contrib import admin

from apps.tracking.models import WeeklyLog


@admin.register(WeeklyLog)
class WeeklyLogAdmin(admin.ModelAdmin):
    list_display = ("internship", "student", "week_start", "submitted_at")
    list_filter = ("week_start", "is_deleted")
    search_fields = ("student__email", "activities", "blockers", "next_steps")
