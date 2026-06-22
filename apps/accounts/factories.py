"""Factories for accounts tests."""

from __future__ import annotations

import factory
from django.contrib.auth import get_user_model

from apps.accounts.models import StaffProfile, StudentProfile
from apps.common.models import UserRole


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda number: f"user{number}@example.com")
    first_name = "Alex"
    last_name = "Martin"
    role = UserRole.STUDENT
    is_active = True
    is_staff = False
    password = factory.PostGenerationMethodCall("set_password", "password")


class StudentProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentProfile

    user = factory.SubFactory(UserFactory, role=UserRole.STUDENT)
    student_number = factory.Sequence(lambda number: f"STU-{number:06d}")
    university = "Université E-CON"
    department = "Informatique"
    program = "Master"
    academic_year = "2025-2026"
    headline = "Étudiant en recherche de stage"
    bio = ""
    skills_summary = ""
    linkedin_url = ""
    github_url = ""
    portfolio_url = ""


class StaffProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffProfile

    user = factory.SubFactory(UserFactory, role=UserRole.ACADEMIC_SUPERVISOR)
    university = "Université E-CON"
    department = "Informatique"
    role_scope = "Encadrement académique"
