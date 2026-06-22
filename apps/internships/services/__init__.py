"""Internship workflow services."""

from apps.common.models import InternshipStatus
from apps.internships.models import Internship


def create_internship_from_application(*, application, academic_supervisor=None) -> Internship:
    internship, _ = Internship.objects.get_or_create(
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
    return internship


def assign_academic_supervisor(
    *, internship: Internship, supervisor=None, supervisor_id=None
) -> Internship:
    internship.academic_supervisor = supervisor
    if supervisor_id is not None:
        internship.academic_supervisor_id = supervisor_id
    internship.status = InternshipStatus.ACTIVE
    internship.save(update_fields=["academic_supervisor", "status", "updated_at"])
    return internship


def complete_internship(*, internship: Internship) -> Internship:
    internship.status = InternshipStatus.COMPLETED
    internship.save(update_fields=["status", "updated_at"])
    return internship
