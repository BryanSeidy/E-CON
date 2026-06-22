"""Internship workflow services."""

from django.core.exceptions import ValidationError

from apps.common.models import InternshipStatus
from apps.internships.models import Internship


def create_internship_from_application(*, application, academic_supervisor=None) -> Internship:
    internship, created = Internship.objects.get_or_create(
        application=application,
        defaults={
            "offer": application.offer,
            "student": application.student,
            "company": application.offer.company,
            "academic_supervisor": academic_supervisor,
            "start_date": application.offer.start_date,
            "end_date": application.offer.end_date,
        },
    )
    if created:
        from apps.notifications.services import notify

        notify(
            recipient=internship.student,
            title="Internship created",
            message=f"Your internship with {internship.company.name} has been created.",
        )
        if internship.academic_supervisor_id:
            notify(
                recipient=internship.academic_supervisor,
                title="Internship supervision assigned",
                message=f"You have been assigned to supervise {internship.student.email}.",
            )
    return internship


def assign_academic_supervisor(
    *, internship: Internship, supervisor=None, supervisor_id=None
) -> Internship:
    if internship.status not in {InternshipStatus.ASSIGNED, InternshipStatus.ACTIVE}:
        raise ValidationError("Supervisor can only be assigned before internship completion.")
    internship.academic_supervisor = supervisor
    if supervisor_id is not None:
        internship.academic_supervisor_id = supervisor_id
    internship.status = InternshipStatus.ACTIVE
    internship.save(update_fields=["academic_supervisor", "status", "updated_at"])
    return internship


def complete_internship(*, internship: Internship) -> Internship:
    if internship.status != InternshipStatus.ACTIVE:
        raise ValidationError("Only active internships can be completed.")
    internship.status = InternshipStatus.COMPLETED
    internship.save(update_fields=["status", "updated_at"])
    return internship
