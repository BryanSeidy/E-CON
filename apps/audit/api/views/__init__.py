"""Audit API views exposing the current auditable context."""

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.api.serializers import AuditContextSerializer
from apps.common.models import AuditSource


@extend_schema(tags=["audit"], responses=AuditContextSerializer)
class AuditContextView(APIView):
    def get(self, request):
        profile = getattr(request.user, "student_profile", None) or getattr(
            request.user, "staff_profile", None
        )
        tenant = {}
        if profile is not None:
            tenant = {
                "university": getattr(profile, "university", ""),
                "department": getattr(profile, "department", ""),
            }
        data = {
            "actor_id": request.user.id,
            "actor_email": request.user.email,
            "actor_role": request.user.role,
            "source": AuditSource.API,
            "tenant": tenant,
        }
        return Response(AuditContextSerializer(data).data)
