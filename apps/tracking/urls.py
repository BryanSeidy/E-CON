"""Tracking routes."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.tracking.api.views import WeeklyLogViewSet

router = DefaultRouter()
router.register("weekly-logs", WeeklyLogViewSet, basename="weekly-log")
urlpatterns = [path("", include(router.urls))]
