"""Evaluation viewsets."""

from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.common.models import UserRole
from apps.evaluations.api.serializers import EvaluationSerializer
from apps.evaluations.models import Evaluation
from apps.evaluations.permissions import CanManageEvaluations
from apps.evaluations.selectors import evaluation_list_for_user
from apps.evaluations.services import submit_evaluation


@extend_schema(tags=["evaluations"])
class EvaluationViewSet(ModelViewSet):
    queryset = Evaluation.objects.none()
    serializer_class = EvaluationSerializer
    permission_classes = [CanManageEvaluations]

    def get_queryset(self):
        return evaluation_list_for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        internship = serializer.validated_data["internship"]
        if (
            request.user.role == UserRole.COMPANY_MEMBER
            and not internship.company.memberships.filter(user=request.user).exists()
        ):
            raise PermissionDenied("Cannot evaluate this internship.")
        if (
            request.user.role == UserRole.ACADEMIC_SUPERVISOR
            and internship.academic_supervisor_id != request.user.id
        ):
            raise PermissionDenied("Cannot evaluate this internship.")
        try:
            evaluation = submit_evaluation(
                internship=internship,
                evaluator=request.user,
                evaluation_type=serializer.validated_data["evaluation_type"],
                score=serializer.validated_data["score"],
                comment=serializer.validated_data.get("comment", ""),
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(self.get_serializer(evaluation).data, status=status.HTTP_201_CREATED)
