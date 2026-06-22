"""Notification viewsets."""

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.notifications.api.serializers import NotificationSerializer
from apps.notifications.permissions import CanAccessOwnNotifications
from apps.notifications.selectors import notification_list_for_user
from apps.notifications.services import mark_as_read


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [CanAccessOwnNotifications]

    def get_queryset(self):
        return notification_list_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(recipient=self.request.user)

    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        notification = mark_as_read(notification=self.get_object())
        return Response(self.get_serializer(notification).data)
