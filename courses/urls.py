from django.urls import path
from .views import (
    create_course, 
    EnrollInCourseView, 
    SubmitQuizView, 
    StudentDashboardView,
    TeacherDashboardListView,       # Naya view
    TeacherEnrolledStudentsView     # Naya view
)

urlpatterns = [
    # --- Student aur Course ke Pehle Se Mojud Paths ---
    path('create/', create_course, name='create_course'),
    path('<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='enroll-course'),
    path('<int:course_id>/submit-quiz/', SubmitQuizView.as_view(), name='submit-quiz'),
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    
    # --- Naye Teacher Dashboard ke Paths ---
    path('teacher/dashboard/', TeacherDashboardListView.as_view(), name='teacher-dashboard'),
    path('teacher/course/<int:course_id>/students/', TeacherEnrolledStudentsView.as_view(), name='teacher-enrolled-students'),
]