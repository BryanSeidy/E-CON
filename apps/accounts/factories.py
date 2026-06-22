"""Factories for accounts tests."""

from __future__ import annotations

from itertools import count
from typing import Any

from django.contrib.auth import get_user_model

from apps.accounts.models import StaffProfile, StudentProfile
from apps.common.models import UserRole

_sequence = count(1)


class UserFactory:
    """Small test factory for users without external runtime dependencies."""

    @classmethod
    def create(cls, **kwargs: Any):
        number = next(_sequence)
        defaults = {
            "email": f"user{number}@example.com",
            "first_name": "Alex",
            "last_name": "Martin",
            "role": UserRole.STUDENT,
            "is_active": True,
            "is_staff": False,
        }
        defaults.update(kwargs)
        password = defaults.pop("password", "password")
        return get_user_model().objects.create_user(password=password, **defaults)

    def __new__(cls, **kwargs: Any):
        return cls.create(**kwargs)


class StudentProfileFactory:
    """Small test factory for student profiles."""

    @classmethod
    def create(cls, **kwargs: Any) -> StudentProfile:
        number = next(_sequence)
        user = kwargs.pop("user", UserFactory(role=UserRole.STUDENT))
        defaults = {
            "user": user,
            "student_number": f"STU-{number:06d}",
            "university": "Université E-CON",
            "department": "Informatique",
            "program": "Master",
            "academic_year": "2025-2026",
            "headline": "Étudiant en recherche de stage",
            "bio": "",
            "skills_summary": "",
            "linkedin_url": "",
            "github_url": "",
            "portfolio_url": "",
        }
        defaults.update(kwargs)
        return StudentProfile.objects.create(**defaults)

    def __new__(cls, **kwargs: Any) -> StudentProfile:
        return cls.create(**kwargs)


class StaffProfileFactory:
    """Small test factory for staff profiles."""

    @classmethod
    def create(cls, **kwargs: Any) -> StaffProfile:
        user = kwargs.pop("user", UserFactory(role=UserRole.ACADEMIC_SUPERVISOR))
        defaults = {
            "user": user,
            "university": "Université E-CON",
            "department": "Informatique",
            "role_scope": "Encadrement académique",
        }
        defaults.update(kwargs)
        return StaffProfile.objects.create(**defaults)

    def __new__(cls, **kwargs: Any) -> StaffProfile:
        return cls.create(**kwargs)
