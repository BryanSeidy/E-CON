"""Document selectors."""

from apps.common.models import UserRole
from apps.documents.models import Document


def document_list_for_user(user):
    qs = Document.objects.select_related("internship", "uploaded_by", "reviewed_by")
    if user.role == UserRole.STUDENT:
        return qs.filter(uploaded_by=user) | qs.filter(internship__student=user)
    if user.role == UserRole.COMPANY_MEMBER:
        return qs.filter(internship__company__memberships__user=user).distinct()
    if user.role == UserRole.ACADEMIC_SUPERVISOR:
        return qs.filter(internship__academic_supervisor=user)
    return qs
