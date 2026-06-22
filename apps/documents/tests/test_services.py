"""Tests for document services."""

from __future__ import annotations

import uuid

import pytest
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import DocumentStatus, InternshipStatus, UserRole
from apps.companies.models import Company
from apps.documents.models import Document, DocumentType
from apps.documents.services import approve_document, reject_document, submit_document
from apps.internships.models import Internship
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db


def _file(name: str = "doc.pdf") -> ContentFile:
    return ContentFile(b"%PDF-1.4\n%test\n", name=name)


def _make_internship():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    company = Company.objects.create(name=f"DocSvc-{uid}")
    offer = Offer.objects.create(company=company, title="DocSvc Offer", description="D")
    application = Application.objects.create(offer=offer, student=student)
    internship = Internship.objects.create(
        application=application,
        offer=offer,
        student=student,
        company=company,
        status=InternshipStatus.ACTIVE,
    )
    return student, internship


class TestApproveDocument:
    def test_approve_uploaded_document(self) -> None:
        student, internship = _make_internship()
        doc = Document.objects.create(
            internship=internship,
            uploaded_by=student,
            title="Report",
            document_type=DocumentType.REPORT,
            file=_file(),
        )
        reviewer = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)

        result = approve_document(document=doc, reviewed_by=reviewer, comment="LGTM")

        assert result.status == DocumentStatus.APPROVED
        assert result.reviewed_by == reviewer
        assert result.comment == "LGTM"

    def test_approve_already_approved_raises(self) -> None:
        student, internship = _make_internship()
        doc = Document.objects.create(
            internship=internship,
            uploaded_by=student,
            title="Report",
            document_type=DocumentType.REPORT,
            file=_file(),
            status=DocumentStatus.APPROVED,
        )
        reviewer = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)

        with pytest.raises(ValidationError):
            approve_document(document=doc, reviewed_by=reviewer)


class TestRejectDocument:
    def test_reject_uploaded_document(self) -> None:
        student, internship = _make_internship()
        doc = Document.objects.create(
            internship=internship,
            uploaded_by=student,
            title="Report",
            document_type=DocumentType.REPORT,
            file=_file(),
        )
        reviewer = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)

        result = reject_document(document=doc, reviewed_by=reviewer, comment="Missing sig")

        assert result.status == DocumentStatus.REJECTED
        assert result.comment == "Missing sig"

    def test_reject_already_rejected_raises(self) -> None:
        student, internship = _make_internship()
        doc = Document.objects.create(
            internship=internship,
            uploaded_by=student,
            title="Report",
            document_type=DocumentType.REPORT,
            file=_file(),
            status=DocumentStatus.REJECTED,
        )
        reviewer = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)

        with pytest.raises(ValidationError):
            reject_document(document=doc, reviewed_by=reviewer)


class TestSubmitDocumentValidation:
    def test_convention_without_internship_raises(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        with pytest.raises(ValidationError):
            submit_document(
                uploaded_by=student,
                title="Convention",
                file=_file("convention.pdf"),
                document_type=DocumentType.CONVENTION,
            )
