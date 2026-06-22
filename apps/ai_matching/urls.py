"""AI matching routes."""

from django.urls import path

from apps.ai_matching.api.views import OfferRecommendationListView

urlpatterns = [
    path(
        "ai-matching/offers/",
        OfferRecommendationListView.as_view(),
        name="ai-offer-matches",
    )
]
