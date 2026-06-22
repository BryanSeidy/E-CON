"""Document admin."""

from django.contrib import admin

from apps.documents.models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "internship", "uploaded_by", "status")
    list_filter = ("status", "is_deleted")
    search_fields = ("title", "uploaded_by__email", "comment")
