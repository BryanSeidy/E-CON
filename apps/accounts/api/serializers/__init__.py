"""JWT serializers for email-based authentication."""

from __future__ import annotations

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EconTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Accept email/password and embed role claims in the JWT."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        return token

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields["email"] = self.fields.pop("username")
