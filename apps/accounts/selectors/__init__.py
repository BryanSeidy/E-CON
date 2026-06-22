"""Account selectors."""

from django.db.models import Count

from apps.accounts.models import User
from apps.common.models import UserRole


def university_students_for_user(user):
    qs = (
        User.objects.filter(role=UserRole.STUDENT)
        .select_related("student_profile")
        .annotate(
            applications_count=Count("applications", distinct=True),
            internships_count=Count("student_internships", distinct=True),
        )
    )
    if user.role == UserRole.SUPER_ADMIN:
        return qs
    staff_profile = getattr(user, "staff_profile", None)
    if staff_profile is None:
        return qs.none()
    qs = qs.filter(student_profile__university=staff_profile.university)
    if user.role in {UserRole.HEAD_OF_PROGRAM, UserRole.ACADEMIC_SUPERVISOR}:
        qs = qs.filter(student_profile__department=staff_profile.department)
    return qs
