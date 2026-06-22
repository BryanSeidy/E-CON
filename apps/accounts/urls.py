"""Account routes."""

from django.urls import path

from apps.accounts.api.views import CurrentUserProfileView, UniversityStudentListView

urlpatterns = [
    path("profile/", CurrentUserProfileView.as_view(), name="current-user-profile"),
    path("university/students/", UniversityStudentListView.as_view(), name="university-students"),
]
