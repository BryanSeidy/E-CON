"""Company admin."""

from django.contrib import admin

from apps.companies.models import Company, CompanyMembership


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "is_active")
    list_filter = ("is_active", "country", "is_deleted")
    search_fields = ("name", "city", "country")


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ("company", "user", "title", "is_owner")
    list_filter = ("company", "is_owner", "is_deleted")
    search_fields = ("company__name", "user__email", "title")
