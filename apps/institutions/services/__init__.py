"""Institution services."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.institutions.models import Department, Institution


def create_institution(*, name: str, code: str, country: str = "", city: str = "") -> Institution:
    try:
        return Institution.objects.create(name=name, code=code, country=country, city=city)
    except IntegrityError as exc:
        raise ValidationError(
            f"An institution with the name '{name}' or code '{code}' already exists."
        ) from exc


def create_department(*, institution: Institution, name: str, code: str) -> Department:
    try:
        return Department.objects.create(institution=institution, name=name, code=code)
    except IntegrityError as exc:
        raise ValidationError(
            f"A department with code '{code}' already exists in this institution."
        ) from exc
