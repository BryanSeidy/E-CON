"""Critical RBAC and tenant filtering tests."""

from __future__ import annotations

import pytest
from apps.applications.api.views import ApplicationViewSet
from apps.applications.models import Application
from apps.common.models import ApplicationStatus, DocumentStatus, InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.documents.api.views import DocumentViewSet
from apps.documents.models import Document, DocumentType
from apps.internships.models import Internship
from apps.offers.api.views import OfferViewSet
from apps.offers.models import Offer
from config.dashboard import StudentDashboardView
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework.test import APIRequestFactory, force_authenticate

pytestmark = pytest.mark.django_db


def _user(email: str, role: str):
    return get_user_model().objects.create_user(email=email, password="pass", role=role)


def _file(name: str = "document.pdf") -> ContentFile:
    return ContentFile(b"%PDF-1.4\n%test\n", name=name)


def _setup_company_flow():
    student = _user("student-rbac@econ.test", UserRole.STUDENT)
    other_student = _user("other-student-rbac@econ.test", UserRole.STUDENT)
    company_member = _user("company-rbac@econ.test", UserRole.COMPANY_MEMBER)
    other_company_member = _user("other-company-rbac@econ.test", UserRole.COMPANY_MEMBER)
    company = Company.objects.create(name="RBAC Company")
    other_company = Company.objects.create(name="Other RBAC Company")
    CompanyMembership.objects.create(company=company, user=company_member)
    CompanyMembership.objects.create(company=other_company, user=other_company_member)
    offer = Offer.objects.create(company=company, title="RBAC Offer", description="Secure")
    other_offer = Offer.objects.create(
        company=other_company, title="Other Offer", description="Secure"
    )
    application = Application.objects.create(offer=offer, student=student)
    other_application = Application.objects.create(offer=other_offer, student=other_student)
    internship = Internship.objects.create(
        application=application,
        offer=offer,
        student=student,
        company=company,
        status=InternshipStatus.ACTIVE,
    )
    return (
        student,
        other_student,
        company_member,
        other_company_member,
        offer,
        application,
        other_application,
        internship,
    )


def test_student_cannot_read_another_students_application() -> None:
    factory = APIRequestFactory()
    data = _setup_company_flow()
    student = data[0]
    application = data[6]
    view = ApplicationViewSet.as_view({"get": "retrieve"})
    request = factory.get(f"/api/v1/applications/{application.id}/")
    force_authenticate(request, user=student)

    response = view(request, pk=application.id)

    assert response.status_code == 404


def test_company_member_cannot_accept_other_company_application() -> None:
    factory = APIRequestFactory()
    data = _setup_company_flow()
    company_member = data[2]
    other_application = data[6]
    view = ApplicationViewSet.as_view({"post": "accept"})
    request = factory.post(f"/api/v1/applications/{other_application.id}/accept/", {})
    force_authenticate(request, user=company_member)

    response = view(request, pk=other_application.id)

    assert response.status_code == 404
    other_application.refresh_from_db()
    assert other_application.status == ApplicationStatus.PENDING


def test_company_member_cannot_create_offer_for_another_company() -> None:
    factory = APIRequestFactory()
    data = _setup_company_flow()
    company_member = data[2]
    other_company = Company.objects.get(name="Other RBAC Company")
    view = OfferViewSet.as_view({"post": "create"})
    request = factory.post(
        "/api/v1/offers/",
        {"company": str(other_company.id), "title": "Forbidden", "description": "No"},
        format="json",
    )
    force_authenticate(request, user=company_member)

    response = view(request)

    assert response.status_code == 403


def test_student_cannot_reject_document() -> None:
    factory = APIRequestFactory()
    student, *_rest, internship = _setup_company_flow()
    document = Document.objects.create(
        internship=internship,
        uploaded_by=student,
        title="Report",
        document_type=DocumentType.REPORT,
        file=_file("report.pdf"),
    )
    view = DocumentViewSet.as_view({"post": "reject"})
    request = factory.post(f"/api/v1/documents/{document.id}/reject/", {})
    force_authenticate(request, user=student)

    response = view(request, pk=document.id)

    assert response.status_code == 403
    document.refresh_from_db()
    assert document.status == DocumentStatus.UPLOADED


def test_student_dashboard_is_role_scoped() -> None:
    factory = APIRequestFactory()
    company_member = _user("dash-company@econ.test", UserRole.COMPANY_MEMBER)
    view = StudentDashboardView.as_view()
    request = factory.get("/dashboard/student/")
    force_authenticate(request, user=company_member)

    response = view(request)

    assert response.status_code == 403
