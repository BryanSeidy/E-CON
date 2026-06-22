"""Internship admin."""

from django.contrib import admin

from apps.internships.models import Internship


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ("student", "company", "academic_supervisor", "status", "start_date", "end_date")
    list_filter = ("status", "company", "is_deleted")
    search_fields = ("student__email", "company__name", "offer__title")
