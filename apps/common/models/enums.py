"""Centralized domain and technical enums.

These enums are infrastructure contracts only. They mirror the validated CDC
roles and workflows without adding business states.
"""

from __future__ import annotations

from django.db import models


class UserRole(models.TextChoices):
    """Official roles validated by the CDC."""

    SUPER_ADMIN = "SUPER_ADMIN", "Super admin"
    UNIVERSITY_ADMIN = "UNIVERSITY_ADMIN", "University admin"
    HEAD_OF_PROGRAM = "HEAD_OF_PROGRAM", "Head of program"
    ACADEMIC_SUPERVISOR = "ACADEMIC_SUPERVISOR", "Academic supervisor"
    STUDENT = "STUDENT", "Student"
    COMPANY_MEMBER = "COMPANY_MEMBER", "Company member"


class ProgramLevel(models.TextChoices):
    """Academic levels supported by the MVP."""

    BTS = "BTS", "BTS"
    LICENCE = "LICENCE", "Licence"
    MASTER = "MASTER", "Master"


class ApplicationStatus(models.TextChoices):
    """Validated application workflow states."""

    PENDING = "PENDING", "Pending"
    REVIEWED = "REVIEWED", "Reviewed"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"


class InternshipStatus(models.TextChoices):
    """Validated internship workflow states."""

    ASSIGNED = "ASSIGNED", "Assigned"
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class ConventionStatus(models.TextChoices):
    """Validated convention workflow states."""

    GENERATED = "GENERATED", "Generated"
    DOWNLOADED = "DOWNLOADED", "Downloaded"
    SIGNED = "SIGNED", "Signed"
    APPROVED = "APPROVED", "Approved"


class DocumentStatus(models.TextChoices):
    """Validated document workflow states."""

    UPLOADED = "UPLOADED", "Uploaded"
    IN_REVIEW = "IN_REVIEW", "In review"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class EvaluationType(models.TextChoices):
    """Evaluation categories validated for the MVP."""

    ACADEMIC = "ACADEMIC", "Academic"
    PROFESSIONAL = "PROFESSIONAL", "Professional"


class AIProcessingStatus(models.TextChoices):
    """Technical processing states for asynchronous AI tasks."""

    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class AuditSource(models.TextChoices):
    """Sources that can produce audit events."""

    API = "API", "API"
    CELERY = "CELERY", "Celery"
    SYSTEM = "SYSTEM", "System"
