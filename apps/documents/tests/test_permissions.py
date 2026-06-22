"""Tests for document permissions."""

from __future__ import annotations

import uuid
from unittest.mock import Mock

import pytest
from django.core.files.base import ContentFile
from rest_framework.test import APIRequestFactory

from apps.accounts.factories import UserFactory
from apps.applications.models import Application
from apps.common.models import InternshipStatus, UserRole
from apps.companies.models import Company, CompanyMembership
from apps.documents.models import Document, DocumentType
from apps.documents.permissions import CanAccessDocuments
from apps.internships.models import Internship
from apps.offers.models import Offer

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


def _file(name: str = "doc.pdf") -> ContentFile:
    return ContentFile(b"%PDF-1.4\n%test\n", name=name)


def _make_doc():
    uid = uuid.uuid4().hex[:8]
    student = UserFactory(role=UserRole.STUDENT)
    supervisor = UserFactory(role=UserRole.ACADEMIC_SUPERVISOR)
    company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
    company = Company.objects.create(name=f"DocPerm-{uid}")
    CompanyMembership.objects.create(company=company, user=company_user)
    offer = Offer.objects.create(company=company, title="Doc Perm Offer", description="D")
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
    standalone_doc = Document.objects.create(
        uploaded_by=student,
        title="CV",
        document_type=DocumentType.CV,
        file=_file("cv.pdf"),
    )
    return student, supervisor, company_user, doc, standalone_doc


class TestCanAccessDocuments:
    def _perm(self) -> CanAccessDocuments:
        return CanAccessDocuments()

    def test_unauthenticated_denied(self) -> None:
        from django.contrib.auth.models import AnonymousUser

        request = factory.get("/")
        request.user = AnonymousUser()
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is False

    def test_create_only_for_students(self) -> None:
        student = UserFactory(role=UserRole.STUDENT)
        request = factory.post("/")
        request.user = student
        view = Mock(action="create")
        assert self._perm().has_permission(request, view) is True

    def test_create_denied_for_non_students(self) -> None:
        company_user = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.post("/")
        request.user = company_user
        view = Mock(action="create")
        assert self._perm().has_permission(request, view) is False

    def test_list_allowed_for_any_authenticated(self) -> None:
        user = UserFactory(role=UserRole.COMPANY_MEMBER)
        request = factory.get("/")
        request.user = user
        view = Mock(action="list")
        assert self._perm().has_permission(request, view) is True

    def test_object_super_admin_allowed(self) -> None:
        admin = UserFactory(role=UserRole.SUPER_ADMIN)
        _stu, _sup, _co, doc, _standalone = _make_doc()
        request = factory.put("/")
        request.user = admin
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, doc) is True

    def test_object_student_read_own(self) -> None:
        student, _sup, _co, doc, _standalone = _make_doc()
        request = factory.get("/")
        request.user = student
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, doc) is True

    def test_object_student_write_denied(self) -> None:
        student, _sup, _co, doc, _standalone = _make_doc()
        request = factory.put("/")
        request.user = student
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, doc) is False

    def test_object_supervisor_allowed(self) -> None:
        _stu, supervisor, _co, doc, _standalone = _make_doc()
        request = factory.get("/")
        request.user = supervisor
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, doc) is True

    def test_object_company_member_allowed(self) -> None:
        _stu, _sup, company_user, doc, _standalone = _make_doc()
        request = factory.get("/")
        request.user = company_user
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, doc) is True

    def test_object_standalone_doc_uploader_allowed(self) -> None:
        student, _sup, _co, _doc, standalone = _make_doc()
        request = factory.get("/")
        request.user = student
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, standalone) is True

    def test_object_standalone_doc_non_uploader_denied(self) -> None:
        _stu, _sup, company_user, _doc, standalone = _make_doc()
        request = factory.get("/")
        request.user = company_user
        view = Mock(action="retrieve")
        assert self._perm().has_object_permission(request, view, standalone) is False

    def test_object_head_of_program_allowed(self) -> None:
        hop = UserFactory(role=UserRole.HEAD_OF_PROGRAM)
        _stu, _sup, _co, doc, _standalone = _make_doc()
        request = factory.put("/")
        request.user = hop
        view = Mock(action="update")
        assert self._perm().has_object_permission(request, view, doc) is True
