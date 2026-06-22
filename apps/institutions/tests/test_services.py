"""Tests for institution services."""

from __future__ import annotations

import uuid

import pytest

from apps.institutions.models import Department, Institution
from apps.institutions.services import create_department, create_institution

pytestmark = pytest.mark.django_db


class TestCreateInstitution:
    def test_creates_institution(self) -> None:
        uid = uuid.uuid4().hex[:8]
        inst = create_institution(name=f"Uni-{uid}", code=f"UT{uid[:4]}")
        assert f"Uni-{uid}" == inst.name
        assert Institution.objects.filter(id=inst.id).exists()

    def test_creates_institution_with_location(self) -> None:
        uid = uuid.uuid4().hex[:8]
        inst = create_institution(
            name=f"MIT-{uid}", code=f"MIT{uid[:4]}", country="US", city="Cambridge"
        )
        assert inst.country == "US"
        assert inst.city == "Cambridge"


class TestCreateDepartment:
    def test_creates_department(self) -> None:
        uid = uuid.uuid4().hex[:8]
        inst = create_institution(name=f"UniDept-{uid}", code=f"UD{uid[:4]}")
        dept = create_department(institution=inst, name="CS", code=f"CS{uid[:4]}")
        assert dept.name == "CS"
        assert dept.institution == inst
        assert Department.objects.filter(id=dept.id).exists()
