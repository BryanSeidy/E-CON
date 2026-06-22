"""Offer routes."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.offers.api.views import OfferViewSet

router = DefaultRouter()
router.register("offers", OfferViewSet)
urlpatterns = [path("", include(router.urls))]
