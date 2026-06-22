"""Evaluation services."""

from django.utils import timezone

from apps.evaluations.models import Evaluation


def submit_evaluation(
    *, internship, evaluator, evaluation_type: str, score: int, comment: str = ""
) -> Evaluation:
    evaluation, _ = Evaluation.objects.update_or_create(
        internship=internship,
        evaluation_type=evaluation_type,
        defaults={
            "evaluator": evaluator,
            "score": score,
            "comment": comment,
            "submitted_at": timezone.now(),
        },
    )
    return evaluation
