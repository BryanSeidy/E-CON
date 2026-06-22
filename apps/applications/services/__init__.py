"""Application workflow services."""

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.applications.models import Application
from apps.common.models import ApplicationStatus
from apps.internships.services import create_internship_from_application


def submit_application(*, offer, student, cover_letter: str = "") -> Application:
    if not offer.is_active:
        raise ValidationError("Cannot apply to an inactive offer.")
    application, created = Application.objects.get_or_create(
        offer=offer, student=student, defaults={"cover_letter": cover_letter}
    )
    if not created and application.status != ApplicationStatus.PENDING:
        raise ValidationError("Cannot update an application after review.")
    if created:
        from apps.notifications.services import notify

        for membership in offer.company.memberships.select_related("user"):
            notify(
                recipient=membership.user,
                title="New application",
                message=f"{student.email} applied to {offer.title}.",
            )
    return application


@transaction.atomic
def accept_application(*, application: Application, reviewed_by, academic_supervisor=None):
    if application.status != ApplicationStatus.PENDING:
        raise ValidationError("Only pending applications can be accepted.")
    application.status = ApplicationStatus.ACCEPTED
    application.reviewed_by = reviewed_by
    application.reviewed_at = timezone.now()
    application.save(update_fields=["status", "reviewed_by", "reviewed_at", "updated_at"])

    from apps.notifications.services import notify

    notify(
        recipient=application.student,
        title="Application accepted",
        message=f"Your application for {application.offer.title} was accepted.",
    )
    return create_internship_from_application(
        application=application, academic_supervisor=academic_supervisor
    )


def reject_application(*, application: Application, reviewed_by) -> Application:
    if application.status != ApplicationStatus.PENDING:
        raise ValidationError("Only pending applications can be rejected.")
    application.status = ApplicationStatus.REJECTED
    application.reviewed_by = reviewed_by
    application.reviewed_at = timezone.now()
    application.save(update_fields=["status", "reviewed_by", "reviewed_at", "updated_at"])
    return application
