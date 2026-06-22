"""Evaluation services."""

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.common.models import InternshipStatus
from apps.evaluations.models import Evaluation


def submit_evaluation(
    *, internship, evaluator, evaluation_type: str, score: int, comment: str = ""
) -> Evaluation:
    if internship.status != InternshipStatus.ACTIVE:
        raise ValidationError("Evaluations can only be submitted for active internships.")
    evaluation, created = Evaluation.objects.update_or_create(
        internship=internship,
        evaluation_type=evaluation_type,
        defaults={
            "evaluator": evaluator,
            "score": score,
            "comment": comment,
            "submitted_at": timezone.now(),
        },
    )
    if created:
        from apps.notifications.services import notify

        notify(
            recipient=internship.student,
            title="Evaluation submitted",
            message=(
                f"An evaluation was submitted for your internship with {internship.company.name}."
            ),
        )
    return evaluation
