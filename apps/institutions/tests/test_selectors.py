"""Tests for institution selectors."""

from __future__ import annotations

import uuid

import pytest

from apps.institutions.models import Department, Institution
from apps.institutions.selectors import department_list, institution_list

pytestmark = pytest.mark.django_db


class TestInstitutionList:
    def test_returns_active_institutions(self) -> None:
        uid = uuid.uuid4().hex[:8]
        Institution.objects.create(name=f"Active-{uid}", code=f"ACT{uid[:4]}", is_active=True)
        Institution.objects.create(name=f"Inactive-{uid}", code=f"INA{uid[:4]}", is_active=False)

        qs = institution_list()
        names = list(qs.values_list("name", flat=True))
        assert f"Active-{uid}" in names
        assert f"Inactive-{uid}" not in names


class TestDepartmentList:
    def test_returns_all_departments(self) -> None:
        uid = uuid.uuid4().hex[:8]
        inst = Institution.objects.create(name=f"Uni-{uid}", code=f"UNI{uid[:4]}")
        Department.objects.create(institution=inst, name="CS", code=f"CS{uid[:4]}")
        Department.objects.create(institution=inst, name="Math", code=f"MTH{uid[:4]}")

        qs = department_list()
        assert qs.filter(institution=inst).count() == 2
