"""
Integration QA – 10 critical flows exercised through the DRF API layer.

Each test class covers one user-facing flow end-to-end using APIClient
and real DB objects (in-memory SQLite). Bugs are surfaced as test failures.
"""

from __future__ import annotations

import uuid
from datetime import date, timedelta
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import StaffProfile, StudentProfile, User
from apps.applications.models import Application
from apps.common.models import (
    ApplicationStatus,
    DocumentStatus,
    EvaluationType,  # ACADEMIC, PROFESSIONAL
    InternshipStatus,
    UserRole,
)
from apps.companies.models import Company, CompanyMembership
from apps.documents.models import Document
from apps.evaluations.models import Evaluation
from apps.institutions.models import Department, Institution
from apps.internships.models import Internship
from apps.notifications.models import Notification
from apps.offers.models import Offer
from apps.tracking.models import WeeklyLog

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _uid():
    return uuid.uuid4().hex[:8]


def _make_student(password="Testpass1!"):
    uid = _uid()
    user = User.objects.create_user(
        email=f"student-{uid}@test.com",
        password=password,
        role=UserRole.STUDENT,
        first_name="Student",
        last_name=uid,
    )
    StudentProfile.objects.create(
        user=user,
        student_number=f"STU-{uid}",
        university="Test Uni",
        department="CS",
        program="BSc CS",
        academic_year="2025",
        skills_summary="python, django, react",
    )
    return user


def _make_company_user(company=None, password="Testpass1!"):
    uid = _uid()
    user = User.objects.create_user(
        email=f"company-{uid}@test.com",
        password=password,
        role=UserRole.COMPANY_MEMBER,
        first_name="CompanyUser",
        last_name=uid,
    )
    if company is None:
        company = Company.objects.create(name=f"Co-{uid}")
    CompanyMembership.objects.create(company=company, user=user)
    return user, company


def _make_supervisor(password="Testpass1!"):
    uid = _uid()
    user = User.objects.create_user(
        email=f"supervisor-{uid}@test.com",
        password=password,
        role=UserRole.ACADEMIC_SUPERVISOR,
        first_name="Supervisor",
        last_name=uid,
    )
    StaffProfile.objects.create(
        user=user,
        university="Test Uni",
        department="CS",
        role_scope="Supervisor",
    )
    return user


def _make_admin(password="Testpass1!"):
    uid = _uid()
    return User.objects.create_user(
        email=f"admin-{uid}@test.com",
        password=password,
        role=UserRole.SUPER_ADMIN,
        first_name="Admin",
        last_name=uid,
    )


def _make_univ_admin(password="Testpass1!"):
    uid = _uid()
    user = User.objects.create_user(
        email=f"univadmin-{uid}@test.com",
        password=password,
        role=UserRole.UNIVERSITY_ADMIN,
        first_name="UnivAdmin",
        last_name=uid,
    )
    StaffProfile.objects.create(
        user=user,
        university="Test Uni",
        department="CS",
        role_scope="Admin",
    )
    return user


def _make_offer(company, **kwargs):
    defaults = dict(
        title=f"Offer-{_uid()}",
        description="Test offer description",
        location="Paris",
        required_skills="python, django",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=90),
        is_active=True,
    )
    defaults.update(kwargs)
    return Offer.objects.create(company=company, **defaults)


def _auth_client(user, password="Testpass1!"):
    """Get an authenticated APIClient using JWT token."""
    client = APIClient()
    resp = client.post(
        "/api/v1/auth/token/",
        {"email": user.email, "password": password},
        format="json",
    )
    assert resp.status_code == status.HTTP_200_OK, (
        f"Login failed for {user.email}: {resp.data}"
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
    return client


def _pdf_file(name="test.pdf"):
    return SimpleUploadedFile(name, b"%PDF-1.4 test content", content_type="application/pdf")


# ===========================================================================
# Flow 1: Login
# ===========================================================================

class TestFlow01Login:
    """JWT login via /api/v1/auth/token/"""

    def test_student_login_returns_tokens(self):
        student = _make_student()
        client = APIClient()
        resp = client.post(
            "/api/v1/auth/token/",
            {"email": student.email, "password": "Testpass1!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access" in resp.data
        assert "refresh" in resp.data

    def test_company_login_returns_tokens(self):
        user, _ = _make_company_user()
        client = APIClient()
        resp = client.post(
            "/api/v1/auth/token/",
            {"email": user.email, "password": "Testpass1!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access" in resp.data

    def test_admin_login_returns_tokens(self):
        admin = _make_admin()
        client = APIClient()
        resp = client.post(
            "/api/v1/auth/token/",
            {"email": admin.email, "password": "Testpass1!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access" in resp.data

    def test_wrong_password_fails(self):
        student = _make_student()
        client = APIClient()
        resp = client.post(
            "/api/v1/auth/token/",
            {"email": student.email, "password": "wrong"},
            format="json",
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh(self):
        student = _make_student()
        client = APIClient()
        resp = client.post(
            "/api/v1/auth/token/",
            {"email": student.email, "password": "Testpass1!"},
            format="json",
        )
        refresh = resp.data["refresh"]
        resp2 = client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": refresh},
            format="json",
        )
        assert resp2.status_code == status.HTTP_200_OK
        assert "access" in resp2.data

    def test_unauthenticated_profile_rejected(self):
        client = APIClient()
        resp = client.get("/api/v1/profile/")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ===========================================================================
# Flow 2: Dashboard by role
# ===========================================================================

class TestFlow02Dashboard:
    """Dashboard endpoints per role."""

    def test_student_dashboard(self):
        student = _make_student()
        client = _auth_client(student)
        resp = client.get("/dashboard/student/")
        assert resp.status_code == status.HTTP_200_OK
        assert "applications" in resp.data
        assert "pending_applications" in resp.data
        assert "weekly_logs" in resp.data

    def test_company_dashboard(self):
        user, company = _make_company_user()
        client = _auth_client(user)
        resp = client.get("/dashboard/company/")
        assert resp.status_code == status.HTTP_200_OK
        assert "active_offers" in resp.data
        assert "applications" in resp.data

    def test_university_dashboard_as_supervisor(self):
        supervisor = _make_supervisor()
        client = _auth_client(supervisor)
        resp = client.get("/dashboard/university/")
        assert resp.status_code == status.HTTP_200_OK
        assert "assigned_internships" in resp.data
        assert "documents_to_review" in resp.data

    def test_university_dashboard_as_univ_admin(self):
        admin = _make_univ_admin()
        client = _auth_client(admin)
        resp = client.get("/dashboard/university/")
        assert resp.status_code == status.HTTP_200_OK

    def test_student_cannot_access_company_dashboard(self):
        student = _make_student()
        client = _auth_client(student)
        resp = client.get("/dashboard/company/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_company_user_cannot_access_student_dashboard(self):
        user, _ = _make_company_user()
        client = _auth_client(user)
        resp = client.get("/dashboard/student/")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_access_all_dashboards(self):
        admin = _make_admin()
        client = _auth_client(admin)
        for url in ["/dashboard/student/", "/dashboard/company/", "/dashboard/university/"]:
            resp = client.get(url)
            assert resp.status_code == status.HTTP_200_OK, f"Admin denied on {url}"


# ===========================================================================
# Flow 3: Offer list
# ===========================================================================

class TestFlow03OfferList:
    """Offer CRUD via /api/v1/offers/"""

    def test_student_can_list_offers(self):
        student = _make_student()
        _, company = _make_company_user()
        _make_offer(company)
        client = _auth_client(student)
        resp = client.get("/api/v1/offers/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

    def test_company_member_lists_own_offers(self):
        user, company = _make_company_user()
        _make_offer(company)
        client = _auth_client(user)
        resp = client.get("/api/v1/offers/")
        assert resp.status_code == status.HTTP_200_OK
        # Company member should see own offers
        assert resp.data["count"] >= 1

    def test_company_member_creates_offer(self):
        user, company = _make_company_user()
        client = _auth_client(user)
        resp = client.post(
            "/api/v1/offers/",
            {
                "company": company.id,
                "title": f"New Offer {_uid()}",
                "description": "A great opportunity",
                "location": "Lyon",
                "required_skills": "java, spring",
                "start_date": str(date.today()),
                "end_date": str(date.today() + timedelta(days=60)),
                "is_active": True,
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED, f"Create offer failed: {resp.data}"

    def test_filter_offers_by_active(self):
        _, company = _make_company_user()
        _make_offer(company, is_active=True)
        _make_offer(company, is_active=False)
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.get("/api/v1/offers/?is_active=true")
        assert resp.status_code == status.HTTP_200_OK
        for item in resp.data["results"]:
            assert item["is_active"] is True

    def test_search_offers(self):
        _, company = _make_company_user()
        offer = _make_offer(company, title="UniqueSearchTitle123")
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.get("/api/v1/offers/?search=UniqueSearchTitle123")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1


# ===========================================================================
# Flow 4: Application (candidature)
# ===========================================================================

class TestFlow04Application:
    """Student applies to an offer."""

    def test_student_submits_application(self):
        student = _make_student()
        _, company = _make_company_user()
        offer = _make_offer(company)
        client = _auth_client(student)
        resp = client.post(
            "/api/v1/applications/",
            {"offer": offer.id, "cover_letter": "I'm very interested."},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED, f"Apply failed: {resp.data}"
        assert resp.data["status"] == ApplicationStatus.PENDING

    def test_duplicate_application_prevented(self):
        student = _make_student()
        _, company = _make_company_user()
        offer = _make_offer(company)
        client = _auth_client(student)
        # First application
        resp1 = client.post(
            "/api/v1/applications/",
            {"offer": offer.id, "cover_letter": "First try"},
            format="json",
        )
        assert resp1.status_code == status.HTTP_201_CREATED
        # Second application to same offer – should return existing (idempotent)
        resp2 = client.post(
            "/api/v1/applications/",
            {"offer": offer.id, "cover_letter": "Second try"},
            format="json",
        )
        # The service uses get_or_create so it should be 201 again (or return existing)
        assert resp2.status_code == status.HTTP_201_CREATED
        # Should only be one application
        assert Application.objects.filter(offer=offer, student=student).count() == 1

    def test_application_to_inactive_offer_rejected(self):
        student = _make_student()
        _, company = _make_company_user()
        offer = _make_offer(company, is_active=False)
        client = _auth_client(student)
        resp = client.post(
            "/api/v1/applications/",
            {"offer": offer.id, "cover_letter": "Won't work"},
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_student_sees_own_applications(self):
        student = _make_student()
        _, company = _make_company_user()
        offer = _make_offer(company)
        Application.objects.create(offer=offer, student=student)
        client = _auth_client(student)
        resp = client.get("/api/v1/applications/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

    def test_company_sees_applications_to_its_offers(self):
        student = _make_student()
        user, company = _make_company_user()
        offer = _make_offer(company)
        Application.objects.create(offer=offer, student=student)
        client = _auth_client(user)
        resp = client.get("/api/v1/applications/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1


# ===========================================================================
# Flow 5: Accept / Reject application
# ===========================================================================

class TestFlow05AcceptReject:
    """Company/admin accepts or rejects applications."""

    def test_accept_application_creates_internship(self):
        student = _make_student()
        user, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        client = _auth_client(user)
        resp = client.post(f"/api/v1/applications/{app.id}/accept/")
        assert resp.status_code == status.HTTP_200_OK, f"Accept failed: {resp.data}"
        # Should return internship data
        assert "student" in resp.data
        assert "company" in resp.data
        # Application status should be updated
        app.refresh_from_db()
        assert app.status == ApplicationStatus.ACCEPTED
        # Internship should exist
        assert Internship.objects.filter(application=app).exists()

    def test_reject_application(self):
        student = _make_student()
        user, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        client = _auth_client(user)
        resp = client.post(f"/api/v1/applications/{app.id}/reject/")
        assert resp.status_code == status.HTTP_200_OK, f"Reject failed: {resp.data}"
        app.refresh_from_db()
        assert app.status == ApplicationStatus.REJECTED

    def test_cannot_accept_already_rejected(self):
        student = _make_student()
        user, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(
            offer=offer, student=student, status=ApplicationStatus.REJECTED
        )
        client = _auth_client(user)
        resp = client.post(f"/api/v1/applications/{app.id}/accept/")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_reject_already_accepted(self):
        student = _make_student()
        user, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(
            offer=offer, student=student, status=ApplicationStatus.ACCEPTED
        )
        client = _auth_client(user)
        resp = client.post(f"/api/v1/applications/{app.id}/reject/")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_admin_can_accept(self):
        student = _make_student()
        _, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.post(f"/api/v1/applications/{app.id}/accept/")
        assert resp.status_code == status.HTTP_200_OK


# ===========================================================================
# Flow 6: Internship creation & management
# ===========================================================================

class TestFlow06Internship:
    """Internship lifecycle: creation, supervisor assignment, completion."""

    def _create_internship(self):
        student = _make_student()
        user, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        internship = Internship.objects.create(
            application=app,
            offer=offer,
            student=student,
            company=company,
            start_date=offer.start_date,
            end_date=offer.end_date,
        )
        return student, user, company, internship

    def test_student_sees_own_internships(self):
        student, _, _, internship = self._create_internship()
        client = _auth_client(student)
        resp = client.get("/api/v1/internships/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

    def test_company_sees_its_internships(self):
        _, company_user, _, internship = self._create_internship()
        client = _auth_client(company_user)
        resp = client.get("/api/v1/internships/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

    def test_assign_supervisor(self):
        student, company_user, company, internship = self._create_internship()
        supervisor = _make_supervisor()
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.post(
            f"/api/v1/internships/{internship.id}/assign_supervisor/",
            {"academic_supervisor": supervisor.id},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK, f"Assign supervisor failed: {resp.data}"
        internship.refresh_from_db()
        assert internship.academic_supervisor_id == supervisor.id
        assert internship.status == InternshipStatus.ACTIVE

    def test_complete_internship(self):
        student, company_user, _, internship = self._create_internship()
        # First activate
        internship.status = InternshipStatus.ACTIVE
        internship.save(update_fields=["status"])
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.post(f"/api/v1/internships/{internship.id}/complete/")
        assert resp.status_code == status.HTTP_200_OK, f"Complete failed: {resp.data}"
        internship.refresh_from_db()
        assert internship.status == InternshipStatus.COMPLETED

    def test_cannot_complete_assigned_internship(self):
        student, company_user, _, internship = self._create_internship()
        # Internship defaults to ASSIGNED
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.post(f"/api/v1/internships/{internship.id}/complete/")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ===========================================================================
# Flow 7: Document upload
# ===========================================================================

class TestFlow07DocumentUpload:
    """Document upload, approve, reject via /api/v1/documents/"""

    def _setup_internship(self):
        student = _make_student()
        _, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        internship = Internship.objects.create(
            application=app,
            offer=offer,
            student=student,
            company=company,
        )
        return student, internship

    def test_student_uploads_cv(self):
        student = _make_student()
        client = _auth_client(student)
        resp = client.post(
            "/api/v1/documents/",
            {
                "title": f"My CV {_uid()}",
                "document_type": "CV",
                "file": _pdf_file(),
            },
            format="multipart",
        )
        assert resp.status_code == status.HTTP_201_CREATED, f"Upload failed: {resp.data}"
        assert resp.data["status"] == DocumentStatus.UPLOADED

    def test_student_uploads_convention_needs_internship(self):
        student = _make_student()
        client = _auth_client(student)
        resp = client.post(
            "/api/v1/documents/",
            {
                "title": "Convention",
                "document_type": "CONVENTION",
                "file": _pdf_file("convention.pdf"),
            },
            format="multipart",
        )
        # Convention requires internship
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_student_uploads_convention_with_internship(self):
        student, internship = self._setup_internship()
        client = _auth_client(student)
        resp = client.post(
            "/api/v1/documents/",
            {
                "title": "Convention",
                "document_type": "CONVENTION",
                "internship": internship.id,
                "file": _pdf_file("convention.pdf"),
            },
            format="multipart",
        )
        assert resp.status_code == status.HTTP_201_CREATED, f"Upload convention failed: {resp.data}"

    def test_approve_document(self):
        student, internship = self._setup_internship()
        doc = Document.objects.create(
            uploaded_by=student,
            title="Test Doc",
            document_type="CV",
            file="test.pdf",
        )
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.post(
            f"/api/v1/documents/{doc.id}/approve/",
            {"comment": "Looks good"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK, f"Approve failed: {resp.data}"
        doc.refresh_from_db()
        assert doc.status == DocumentStatus.APPROVED

    def test_reject_document(self):
        student = _make_student()
        doc = Document.objects.create(
            uploaded_by=student,
            title="Bad Doc",
            document_type="CV",
            file="test.pdf",
        )
        admin = _make_admin()
        client = _auth_client(admin)
        resp = client.post(
            f"/api/v1/documents/{doc.id}/reject/",
            {"comment": "Needs revision"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK, f"Reject failed: {resp.data}"
        doc.refresh_from_db()
        assert doc.status == DocumentStatus.REJECTED

    def test_student_sees_own_documents(self):
        student = _make_student()
        Document.objects.create(
            uploaded_by=student,
            title="My Doc",
            document_type="CV",
            file="test.pdf",
        )
        client = _auth_client(student)
        resp = client.get("/api/v1/documents/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1


# ===========================================================================
# Flow 8: Weekly log
# ===========================================================================

class TestFlow08WeeklyLog:
    """Weekly log submission via /api/v1/weekly-logs/"""

    def _setup(self):
        student = _make_student()
        _, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        internship = Internship.objects.create(
            application=app,
            offer=offer,
            student=student,
            company=company,
            status=InternshipStatus.ACTIVE,
        )
        return student, internship

    def test_student_creates_weekly_log(self):
        student, internship = self._setup()
        client = _auth_client(student)
        resp = client.post(
            "/api/v1/weekly-logs/",
            {
                "internship": internship.id,
                "week_start": str(date.today() - timedelta(days=date.today().weekday())),
                "activities": "Worked on API integration",
                "blockers": "None",
                "next_steps": "Continue testing",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED, f"Create log failed: {resp.data}"

    def test_student_sees_own_logs(self):
        student, internship = self._setup()
        WeeklyLog.objects.create(
            internship=internship,
            student=student,
            week_start=date.today(),
            activities="Did stuff",
        )
        client = _auth_client(student)
        resp = client.get("/api/v1/weekly-logs/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

    def test_other_student_cannot_create_log_for_another_internship(self):
        _, internship = self._setup()
        other_student = _make_student()
        client = _auth_client(other_student)
        resp = client.post(
            "/api/v1/weekly-logs/",
            {
                "internship": internship.id,
                "week_start": str(date.today()),
                "activities": "Hacking",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_sees_supervised_logs(self):
        student, internship = self._setup()
        supervisor = _make_supervisor()
        internship.academic_supervisor = supervisor
        internship.save(update_fields=["academic_supervisor"])
        WeeklyLog.objects.create(
            internship=internship,
            student=student,
            week_start=date.today(),
            activities="Work",
        )
        client = _auth_client(supervisor)
        resp = client.get("/api/v1/weekly-logs/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1


# ===========================================================================
# Flow 9: Evaluation
# ===========================================================================

class TestFlow09Evaluation:
    """Evaluation submission via /api/v1/evaluations/"""

    def _setup(self):
        student = _make_student()
        user, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        internship = Internship.objects.create(
            application=app,
            offer=offer,
            student=student,
            company=company,
            status=InternshipStatus.ACTIVE,
        )
        return student, user, company, internship

    def test_company_submits_evaluation(self):
        student, company_user, company, internship = self._setup()
        client = _auth_client(company_user)
        resp = client.post(
            "/api/v1/evaluations/",
            {
                "internship": internship.id,
                "evaluation_type": EvaluationType.PROFESSIONAL,
                "score": 85,
                "comment": "Good work",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED, f"Eval failed: {resp.data}"

    def test_supervisor_submits_evaluation(self):
        student, _, company, internship = self._setup()
        supervisor = _make_supervisor()
        internship.academic_supervisor = supervisor
        internship.save(update_fields=["academic_supervisor"])
        client = _auth_client(supervisor)
        resp = client.post(
            "/api/v1/evaluations/",
            {
                "internship": internship.id,
                "evaluation_type": EvaluationType.ACADEMIC,
                "score": 90,
                "comment": "Excellent",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED, f"Eval failed: {resp.data}"

    def test_evaluation_on_non_active_internship_fails(self):
        student, company_user, company, internship = self._setup()
        internship.status = InternshipStatus.ASSIGNED
        internship.save(update_fields=["status"])
        client = _auth_client(company_user)
        resp = client.post(
            "/api/v1/evaluations/",
            {
                "internship": internship.id,
                "evaluation_type": EvaluationType.PROFESSIONAL,
                "score": 70,
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_student_sees_evaluations(self):
        student, company_user, company, internship = self._setup()
        Evaluation.objects.create(
            internship=internship,
            evaluator=company_user,
            evaluation_type=EvaluationType.PROFESSIONAL,
            score=80,
        )
        client = _auth_client(student)
        resp = client.get("/api/v1/evaluations/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1


# ===========================================================================
# Flow 10: Notifications
# ===========================================================================

class TestFlow10Notifications:
    """Notification lifecycle via /api/v1/notifications/"""

    def test_list_own_notifications(self):
        student = _make_student()
        Notification.objects.create(
            recipient=student,
            title="Welcome",
            message="Welcome to E-CON!",
        )
        client = _auth_client(student)
        resp = client.get("/api/v1/notifications/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

    def test_mark_notification_as_read(self):
        student = _make_student()
        notif = Notification.objects.create(
            recipient=student,
            title="Alert",
            message="Something happened",
        )
        client = _auth_client(student)
        resp = client.post(f"/api/v1/notifications/{notif.id}/read/")
        assert resp.status_code == status.HTTP_200_OK, f"Mark read failed: {resp.data}"
        notif.refresh_from_db()
        assert notif.is_read is True
        assert notif.read_at is not None

    def test_cannot_see_other_users_notifications(self):
        student1 = _make_student()
        student2 = _make_student()
        Notification.objects.create(
            recipient=student1,
            title="Private",
            message="Only for student1",
        )
        client = _auth_client(student2)
        resp = client.get("/api/v1/notifications/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 0

    def test_application_creates_notification_for_company(self):
        """When a student applies, company members should get notified."""
        student = _make_student()
        company_user, company = _make_company_user()
        offer = _make_offer(company)
        client = _auth_client(student)
        resp = client.post(
            "/api/v1/applications/",
            {"offer": offer.id, "cover_letter": "Please consider me"},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        assert Notification.objects.filter(recipient=company_user).exists()

    def test_accept_application_notifies_student(self):
        """When application is accepted, student gets notified."""
        student = _make_student()
        company_user, company = _make_company_user()
        offer = _make_offer(company)
        app = Application.objects.create(offer=offer, student=student)
        client = _auth_client(company_user)
        client.post(f"/api/v1/applications/{app.id}/accept/")
        assert Notification.objects.filter(
            recipient=student, title="Application accepted"
        ).exists()


# ===========================================================================
# Full end-to-end flow: student applies → accepted → internship → docs → logs → eval → notifs
# ===========================================================================

class TestFullE2EFlow:
    """Complete golden path through all 10 flows."""

    def test_golden_path(self):
        # 1. Create users
        student = _make_student()
        company_user, company = _make_company_user()
        supervisor = _make_supervisor()
        admin = _make_admin()

        # 2. Login
        student_client = _auth_client(student)
        company_client = _auth_client(company_user)
        admin_client = _auth_client(admin)

        # 3. Company creates an offer
        resp = company_client.post(
            "/api/v1/offers/",
            {
                "company": company.id,
                "title": f"Full Stack Dev {_uid()}",
                "description": "Build amazing things",
                "location": "Paris",
                "required_skills": "python, django, react",
                "start_date": str(date.today()),
                "end_date": str(date.today() + timedelta(days=120)),
                "is_active": True,
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        offer_id = resp.data["id"]

        # 4. Student lists offers and sees it
        resp = student_client.get("/api/v1/offers/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

        # 5. Student applies
        resp = student_client.post(
            "/api/v1/applications/",
            {"offer": offer_id, "cover_letter": "I'm the best candidate!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        app_id = resp.data["id"]

        # 6. Company sees application
        resp = company_client.get("/api/v1/applications/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] >= 1

        # 7. Company accepts → creates internship
        resp = company_client.post(f"/api/v1/applications/{app_id}/accept/")
        assert resp.status_code == status.HTTP_200_OK
        internship_id = resp.data["id"]

        # 8. Admin assigns supervisor → activates internship
        resp = admin_client.post(
            f"/api/v1/internships/{internship_id}/assign_supervisor/",
            {"academic_supervisor": supervisor.id},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

        # 9. Student uploads a CV document
        resp = student_client.post(
            "/api/v1/documents/",
            {
                "title": f"My CV {_uid()}",
                "document_type": "CV",
                "file": _pdf_file(),
            },
            format="multipart",
        )
        assert resp.status_code == status.HTTP_201_CREATED
        doc_id = resp.data["id"]

        # 10. Admin approves document
        resp = admin_client.post(
            f"/api/v1/documents/{doc_id}/approve/",
            {"comment": "Approved"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

        # 11. Student submits weekly log
        resp = student_client.post(
            "/api/v1/weekly-logs/",
            {
                "internship": internship_id,
                "week_start": str(date.today() - timedelta(days=date.today().weekday())),
                "activities": "Onboarding and environment setup",
                "blockers": "",
                "next_steps": "Start coding",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED

        # 12. Company submits evaluation
        resp = company_client.post(
            "/api/v1/evaluations/",
            {
                "internship": internship_id,
                "evaluation_type": EvaluationType.PROFESSIONAL,
                "score": 88,
                "comment": "Great performance",
            },
            format="json",
        )
        assert resp.status_code == status.HTTP_201_CREATED

        # 13. Check notifications were generated
        resp = student_client.get("/api/v1/notifications/")
        assert resp.status_code == status.HTTP_200_OK
        # Student should have received: application accepted + internship created + evaluation
        assert resp.data["count"] >= 2

        # 14. Mark a notification as read
        if resp.data["results"]:
            notif_id = resp.data["results"][0]["id"]
            resp = student_client.post(f"/api/v1/notifications/{notif_id}/read/")
            assert resp.status_code == status.HTTP_200_OK

        # 15. Dashboards
        resp = student_client.get("/dashboard/student/")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["applications"] >= 1

        resp = company_client.get("/dashboard/company/")
        assert resp.status_code == status.HTTP_200_OK

        # 16. Complete internship
        resp = admin_client.post(f"/api/v1/internships/{internship_id}/complete/")
        assert resp.status_code == status.HTTP_200_OK
