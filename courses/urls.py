from django.urls import path
from .views import create_course, EnrollInCourseView, SubmitQuizView, StudentDashboardView

urlpatterns = [
    path('create/', create_course, name='create_course'),
    path('<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='enroll-course'),
    path('<int:course_id>/submit-quiz/', SubmitQuizView.as_view(), name='submit-quiz'),
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
]