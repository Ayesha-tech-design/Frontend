from django.urls import path
from .views import create_course, EnrollInCourseView, SubmitQuizView # <-- Ye import check karein

urlpatterns = [
    path('create/', create_course, name='create_course'),
    path('<int:course_id>/enroll/', EnrollInCourseView.as_view(), name='enroll-course'),
    
    # Ye wali line shayad missing hai ya galat hai, isay sahi karein:
    path('<int:course_id>/submit-quiz/', SubmitQuizView.as_view(), name='submit-quiz'),
]