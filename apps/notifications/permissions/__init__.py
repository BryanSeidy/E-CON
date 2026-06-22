"""Notification permissions."""

from rest_framework.permissions import BasePermission


class CanAccessOwnNotifications(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.recipient_id == request.user.id
