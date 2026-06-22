"""Application workflow services."""

from django.db import transaction
from django.utils import timezone

from apps.applications.models import Application
from apps.common.models import ApplicationStatus
from apps.internships.services import create_internship_from_application


def submit_application(*, offer, student, cover_letter: str = "") -> Application:
    application, _ = Application.objects.get_or_create(
        offer=offer, student=student, defaults={"cover_letter": cover_letter}
    )
    return application


@transaction.atomic
def accept_application(*, application: Application, reviewed_by, academic_supervisor=None):
    application.status = ApplicationStatus.ACCEPTED
    application.reviewed_by = reviewed_by
    application.reviewed_at = timezone.now()
    application.save(update_fields=["status", "reviewed_by", "reviewed_at", "updated_at"])
    return create_internship_from_application(
        application=application, academic_supervisor=academic_supervisor
    )


def reject_application(*, application: Application, reviewed_by) -> Application:
    application.status = ApplicationStatus.REJECTED
    application.reviewed_by = reviewed_by
    application.reviewed_at = timezone.now()
    application.save(update_fields=["status", "reviewed_by", "reviewed_at", "updated_at"])
    return application
