from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_notes, name='generate_notes'),
]