"""Company selectors."""

from apps.companies.models import Company, CompanyMembership


def company_list():
    return Company.objects.filter(is_active=True)


def memberships_for_user(user):
    return CompanyMembership.objects.filter(user=user).select_related("company", "user")
