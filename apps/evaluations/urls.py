"""Evaluation routes."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.evaluations.api.views import EvaluationViewSet

router = DefaultRouter()
router.register("evaluations", EvaluationViewSet, basename="evaluation")
urlpatterns = [path("", include(router.urls))]
