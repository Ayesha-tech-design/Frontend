from django.urls import path
from . import views

urlpatterns = [
    # Jab frontend '/notes/generate/' par POST request bhejega toh aapka AI chal parega
    path('generate/', views.generate_notes, name='generate_notes'),
]