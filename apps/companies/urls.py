"""Company routes."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.companies.api.views import CompanyMembershipViewSet, CompanyViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet)
router.register("company-memberships", CompanyMembershipViewSet)
urlpatterns = [path("", include(router.urls))]
