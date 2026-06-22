"""Root URL configuration.

Phase D.2 intentionally exposes only operational and schema endpoints.
Business APIs are generated in later phases.
"""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/", include("apps.notifications.urls")),
    path("api/v1/", include("apps.evaluations.urls")),
    path("api/v1/", include("apps.tracking.urls")),
    path("api/v1/", include("apps.documents.urls")),
    path("api/v1/", include("apps.internships.urls")),
    path("api/v1/", include("apps.applications.urls")),
    path("api/v1/", include("apps.offers.urls")),
    path("api/v1/", include("apps.companies.urls")),
    path("api/v1/", include("apps.institutions.urls")),
]
