"""Offer admin."""

from django.contrib import admin

from apps.offers.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "is_active")
    list_filter = ("is_active", "company", "is_deleted")
    search_fields = ("title", "company__name", "description", "required_skills")
