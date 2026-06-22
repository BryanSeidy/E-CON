"""Company services."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import Company, CompanyMembership


def create_company(*, name: str, description: str = "", website: str = "") -> Company:
    try:
        return Company.objects.create(name=name, description=description, website=website)
    except IntegrityError as exc:
        raise ValidationError(f"A company with the name '{name}' already exists.") from exc


def add_company_member(
    *, company: Company, user, title: str = "", is_owner: bool = False
) -> CompanyMembership:
    try:
        return CompanyMembership.objects.create(
            company=company, user=user, title=title, is_owner=is_owner
        )
    except IntegrityError as exc:
        raise ValidationError("This user is already a member of the company.") from exc
