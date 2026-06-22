"""Tracking viewsets."""

from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from apps.tracking.api.serializers import WeeklyLogSerializer
from apps.tracking.permissions import CanAccessWeeklyLogs
from apps.tracking.selectors import weekly_log_list_for_user


class WeeklyLogViewSet(ModelViewSet):
    serializer_class = WeeklyLogSerializer
    permission_classes = [CanAccessWeeklyLogs]

    def get_queryset(self):
        return weekly_log_list_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user, submitted_at=timezone.now())
