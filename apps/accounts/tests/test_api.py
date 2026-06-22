"""Account API tests."""

from __future__ import annotations

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.accounts.api.views import CurrentUserProfileView, UniversityStudentListView
from apps.accounts.factories import StaffProfileFactory, StudentProfileFactory, UserFactory
from apps.common.models import UserRole

pytestmark = pytest.mark.django_db


def test_current_user_profile_patch_updates_user_and_student_profile() -> None:
    user = UserFactory(role=UserRole.STUDENT, first_name="Old")
    StudentProfileFactory(user=user, headline="Old headline", skills_summary="python")
    view = CurrentUserProfileView.as_view()
    request = APIRequestFactory().patch(
        "/api/v1/profile/",
        {
            "first_name": "New",
            "student_profile": {
                "headline": "New headline",
                "skills_summary": "python, django",
            },
        },
        format="json",
    )
    force_authenticate(request, user=user)

    response = view(request)

    assert response.status_code == 200
    user.refresh_from_db()
    user.student_profile.refresh_from_db()
    assert user.first_name == "New"
    assert user.student_profile.headline == "New headline"
    assert user.student_profile.skills_summary == "python, django"


def test_university_students_are_filtered_by_staff_university() -> None:
    staff = UserFactory(role=UserRole.UNIVERSITY_ADMIN)
    StaffProfileFactory(user=staff, university="Université A", department="Info")
    visible = UserFactory(role=UserRole.STUDENT, email="visible@econ.test")
    hidden = UserFactory(role=UserRole.STUDENT, email="hidden@econ.test")
    StudentProfileFactory(user=visible, university="Université A", department="Info")
    StudentProfileFactory(user=hidden, university="Université B", department="Info")
    view = UniversityStudentListView.as_view()
    request = APIRequestFactory().get("/api/v1/university/students/")
    force_authenticate(request, user=staff)

    response = view(request)

    assert response.status_code == 200
    emails = {row["email"] for row in response.data["results"]}
    assert "visible@econ.test" in emails
    assert "hidden@econ.test" not in emails


def test_student_cannot_list_university_students() -> None:
    student = UserFactory(role=UserRole.STUDENT)
    view = UniversityStudentListView.as_view()
    request = APIRequestFactory().get("/api/v1/university/students/")
    force_authenticate(request, user=student)

    response = view(request)

    assert response.status_code == 403
