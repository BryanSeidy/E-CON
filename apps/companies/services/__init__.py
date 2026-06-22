"""Company services."""

from apps.companies.models import Company, CompanyMembership


def create_company(*, name: str, description: str = "", website: str = "") -> Company:
    return Company.objects.create(name=name, description=description, website=website)


def add_company_member(
    *, company: Company, user, title: str = "", is_owner: bool = False
) -> CompanyMembership:
    return CompanyMembership.objects.create(
        company=company, user=user, title=title, is_owner=is_owner
    )
