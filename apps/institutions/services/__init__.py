"""Institution services."""

from apps.institutions.models import Department, Institution


def create_institution(*, name: str, code: str, country: str = "", city: str = "") -> Institution:
    return Institution.objects.create(name=name, code=code, country=country, city=city)


def create_department(*, institution: Institution, name: str, code: str) -> Department:
    return Department.objects.create(institution=institution, name=name, code=code)
