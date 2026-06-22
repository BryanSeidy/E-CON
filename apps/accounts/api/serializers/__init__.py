"""Account API serializers."""

from __future__ import annotations

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import StaffProfile, StudentProfile, User


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


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "student_number",
            "university",
            "department",
            "program",
            "academic_year",
            "headline",
            "bio",
            "skills_summary",
            "linkedin_url",
            "github_url",
            "portfolio_url",
        ]
        read_only_fields = [
            "student_number",
            "university",
            "department",
            "program",
            "academic_year",
        ]


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ["university", "department", "role_scope"]
        read_only_fields = fields


class CurrentUserProfileSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(required=False)
    staff_profile = StaffProfileSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "student_profile",
            "staff_profile",
        ]
        read_only_fields = ["id", "email", "role", "staff_profile"]

    def update(self, instance, validated_data):
        student_profile_data = validated_data.pop("student_profile", None)
        instance = super().update(instance, validated_data)
        if student_profile_data is not None and hasattr(instance, "student_profile"):
            profile = instance.student_profile
            for field, value in student_profile_data.items():
                setattr(profile, field, value)
            profile.save(update_fields=[*student_profile_data.keys(), "updated_at"])
        return instance


class UniversityStudentSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)
    internships_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_active",
            "student_profile",
            "applications_count",
            "internships_count",
        ]
        read_only_fields = fields
