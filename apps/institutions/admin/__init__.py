"""Institution admin."""

from django.contrib import admin

from apps.institutions.models import Department, Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "city", "country", "is_active")
    list_filter = ("is_active", "country", "is_deleted")
    search_fields = ("name", "code", "city")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "institution")
    list_filter = ("institution", "is_deleted")
    search_fields = ("name", "code", "institution__name")
