"""Authentication and account API views."""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.api.serializers import (
    CurrentUserProfileSerializer,
    EconTokenObtainPairSerializer,
    UniversityStudentSerializer,
)
from apps.accounts.permissions import IsUniversityStaff
from apps.accounts.selectors import university_students_for_user


class EconTokenObtainPairView(TokenObtainPairView):
    serializer_class = EconTokenObtainPairSerializer


@extend_schema(tags=["accounts"])
class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CurrentUserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["accounts"])
class UniversityStudentListView(generics.ListAPIView):
    serializer_class = UniversityStudentSerializer
    permission_classes = [IsUniversityStaff]
    search_fields = [
        "email",
        "first_name",
        "last_name",
        "student_profile__student_number",
        "student_profile__program",
    ]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = [
        "email",
        "last_name",
        "student_profile__student_number",
        "created_at",
    ]
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        queryset = university_students_for_user(self.request.user)
        program = self.request.query_params.get("program")
        department = self.request.query_params.get("department")
        if program:
            queryset = queryset.filter(student_profile__program=program)
        if department:
            queryset = queryset.filter(student_profile__department=department)
        return queryset
