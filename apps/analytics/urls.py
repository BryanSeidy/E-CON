"""Analytics routes."""

from django.urls import path

from apps.analytics.api.views import AnalyticsSummaryView

urlpatterns = [
    path("analytics/summary/", AnalyticsSummaryView.as_view(), name="analytics-summary")
]
