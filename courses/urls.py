from django.urls import path
from .views import (
    create_course, 
    EnrollInCourseView, 
    SubmitQuizView, 
    StudentDashboardView,
    TeacherDashboardListView,      
    TeacherEnrolledStudentsView,
    SubmitAssignmentView,          # Naya view import hua
    ViewTeacherAssignmentsView     # Naya view import hua
)

urlpatterns = [
    # --- Student aur Course ke Paths ---
    path('create/', create_course, name='create_course'),
    path('<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='enroll-course'),
    path('<int:course_id>/submit-quiz/', SubmitQuizView.as_view(), name='submit-quiz'),
    path('dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    
    # --- Teacher Dashboard ke Paths ---
    path('teacher/dashboard/', TeacherDashboardListView.as_view(), name='teacher-dashboard'),
    path('teacher/course/<int:course_id>/students/', TeacherEnrolledStudentsView.as_view(), name='teacher-enrolled-students'),

    # --- Zunaira's New Assignment Endpoints ---
    path('<int:course_id>/submit-assignment/', SubmitAssignmentView.as_view(), name='submit-assignment'),
    path('teacher/course/<int:course_id>/assignments/', ViewTeacherAssignmentsView.as_view(), name='view-assignments'),
]