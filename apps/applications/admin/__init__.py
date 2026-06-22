"""Application admin."""

from django.contrib import admin

from apps.applications.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("offer", "student", "status", "reviewed_by", "reviewed_at")
    list_filter = ("status", "offer__company", "is_deleted")
    search_fields = ("offer__title", "student__email", "cover_letter")
