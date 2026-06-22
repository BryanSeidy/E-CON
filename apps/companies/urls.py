"""Company routes."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.companies.api.views import CompanyMembershipViewSet, CompanyViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("company-memberships", CompanyMembershipViewSet, basename="company-membership")
urlpatterns = [path("", include(router.urls))]
