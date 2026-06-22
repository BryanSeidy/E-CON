"""Admin registrations for accounts."""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.accounts.models import StaffProfile, StudentProfile, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Admin for the email-authenticated user model."""

    model = User
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff", "is_deleted")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Identity", {"fields": ("first_name", "last_name", "role")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Soft delete", {"fields": ("is_deleted", "deleted_at", "deleted_by")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "role", "password1", "password2")}),
    )
    readonly_fields = ("created_at", "updated_at", "deleted_at")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student_number",
        "user",
        "university",
        "department",
        "program",
        "academic_year",
    )
    list_filter = ("university", "department", "program", "academic_year", "is_deleted")
    search_fields = ("student_number", "user__email", "user__first_name", "user__last_name")
    readonly_fields = ("created_at", "updated_at", "deleted_at")


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "university", "department", "role_scope")
    list_filter = ("university", "department", "role_scope", "is_deleted")
    search_fields = ("user__email", "user__first_name", "user__last_name", "role_scope")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
