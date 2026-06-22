"""Institution selectors."""

from apps.institutions.models import Department, Institution


def institution_list():
    return Institution.objects.filter(is_active=True)


def department_list():
    return Department.objects.select_related("institution")
