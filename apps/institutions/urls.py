"""Institution routes."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.institutions.api.views import DepartmentViewSet, InstitutionViewSet

router = DefaultRouter()
router.register("institutions", InstitutionViewSet)
router.register("departments", DepartmentViewSet)
urlpatterns = [path("", include(router.urls))]
