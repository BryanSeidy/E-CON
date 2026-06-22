"""Audit routes."""

from django.urls import path

from apps.audit.api.views import AuditContextView

urlpatterns = [path("audit/context/", AuditContextView.as_view(), name="audit-context")]
