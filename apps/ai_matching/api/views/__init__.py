"""AI matching API views backed by existing offer/profile data."""

from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.ai_matching.api.serializers import OfferMatchSerializer
from apps.common.models import UserRole
from apps.offers.models import Offer


@extend_schema(tags=["ai_matching"])
class OfferRecommendationListView(ListAPIView):
    serializer_class = OfferMatchSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        profile = getattr(request.user, "student_profile", None)
        if request.user.role != UserRole.STUDENT or profile is None:
            return Response([])
        student_skills = {
            skill.strip().lower()
            for skill in profile.skills_summary.replace(";", ",").split(",")
            if skill.strip()
        }
        rows = []
        for offer in Offer.objects.filter(is_active=True).select_related("company")[:100]:
            offer_skills = {
                skill.strip().lower()
                for skill in offer.required_skills.replace(";", ",").split(",")
                if skill.strip()
            }
            matched = sorted(student_skills & offer_skills)
            score = (len(matched) / len(offer_skills)) if offer_skills else 0.0
            rows.append(
                {
                    "offer": offer.id,
                    "title": offer.title,
                    "company": offer.company_id,
                    "company_name": offer.company.name,
                    "location": offer.location,
                    "score": round(score, 4),
                    "matched_skills": matched,
                }
            )
        rows.sort(key=lambda item: item["score"], reverse=True)
        serializer = self.get_serializer(rows[:20], many=True)
        return Response(serializer.data)
