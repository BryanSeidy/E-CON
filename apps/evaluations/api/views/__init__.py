"""Evaluation viewsets."""

from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from apps.evaluations.api.serializers import EvaluationSerializer
from apps.evaluations.permissions import CanManageEvaluations
from apps.evaluations.selectors import evaluation_list_for_user


class EvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    permission_classes = [CanManageEvaluations]

    def get_queryset(self):
        return evaluation_list_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(evaluator=self.request.user, submitted_at=timezone.now())
