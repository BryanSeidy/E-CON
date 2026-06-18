"""Foundation smoke tests."""

from __future__ import annotations

from apps.common.models import ApplicationStatus, InternshipStatus, UserRole


def test_validated_roles_are_centralized() -> None:
    """The CDC roles are exposed by the shared enum."""
    assert UserRole.STUDENT == "STUDENT"
    assert UserRole.COMPANY_MEMBER == "COMPANY_MEMBER"


def test_validated_workflows_are_centralized() -> None:
    """Validated workflow statuses are exposed by shared enums."""
    assert ApplicationStatus.PENDING == "PENDING"
    assert InternshipStatus.ACTIVE == "ACTIVE"
