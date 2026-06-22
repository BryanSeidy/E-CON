"""Tracking viewsets."""

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from apps.tracking.api.serializers import WeeklyLogSerializer
from apps.tracking.models import WeeklyLog
from apps.tracking.permissions import CanAccessWeeklyLogs
from apps.tracking.selectors import weekly_log_list_for_user


@extend_schema(tags=["tracking"])
class WeeklyLogViewSet(ModelViewSet):
    queryset = WeeklyLog.objects.none()
    serializer_class = WeeklyLogSerializer
    permission_classes = [CanAccessWeeklyLogs]

    def get_queryset(self):
        return weekly_log_list_for_user(self.request.user)

    def perform_create(self, serializer):
        internship = serializer.validated_data["internship"]
        if internship.student_id != self.request.user.id:
            raise PermissionDenied("Cannot create a weekly log for this internship.")
        serializer.save(student=self.request.user, submitted_at=timezone.now())
