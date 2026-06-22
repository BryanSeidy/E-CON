"""Tests for document selectors."""

from __future__ import annotations

import uuid

import pytest
from django.core.files.base import ContentFile

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.documents.models import Document, DocumentType
from apps.documents.selectors import document_list_for_user
from apps.internships.models import Internship
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db


def _file(name: str = "doc.pdf") -> ContentFile:
    return ContentFile(b"%PDF-1.4\n%test\n", name=name)


def _setup():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    admin = UserFactory(role=UserRole.SUPER_ADMIN)
    company = Company.objects.create(name=f"DocSel-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="Doc Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    internship = Internship.objects.create(
        application=application,
        offer=offer,
        student=student,
        company=company,
        academic_supervisor=supervisor,
        status=InternshipStatus.ACTIVE,
    )
    doc = Document.objects.create(
        internship=internship,
        uploaded_by=student,
        title="Report",
        document_type=DocumentType.REPORT,
        file=_file("report.pdf"),
    )
    cv = Document.objects.create(
        uploaded_by=student,
        title="CV",
        document_type=DocumentType.CV,
        file=_file("cv.pdf"),
    )
    return student, supervisor, company_user, admin, doc, cv


class TestDocumentListForUser:
    def test_student_sees_own_documents(self) -> None:
        student, _sup, _co, _admin, doc, cv = _setup()
        qs = document_list_for_user(student)
        ids = list(qs.values_list("id", flat=True))
        assert doc.id in ids
        assert cv.id in ids

    def test_supervisor_sees_supervised_internship_docs(self) -> None:
        _stu, supervisor, _co, _admin, doc, _cv = _setup()
        qs = document_list_for_user(supervisor)
        assert doc.id in qs.values_list("id", flat=True)

    def test_company_member_sees_company_docs(self) -> None:
        _stu, _sup, company_user, _admin, doc, _cv = _setup()
        qs = document_list_for_user(company_user)
        assert doc.id in qs.values_list("id", flat=True)

    def test_admin_sees_all_docs(self) -> None:
        _stu, _sup, _co, admin, doc, cv = _setup()
        qs = document_list_for_user(admin)
        ids = list(qs.values_list("id", flat=True))
        assert doc.id in ids
        assert cv.id in ids
