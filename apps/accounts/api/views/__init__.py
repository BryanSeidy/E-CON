"""Authentication API views."""

from __future__ import annotations

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.api.serializers import EconTokenObtainPairSerializer


class EconTokenObtainPairView(TokenObtainPairView):
    serializer_class = EconTokenObtainPairSerializer
