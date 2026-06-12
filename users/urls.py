from django.urls import path
from .views import signup, login_check
from django.urls import path
from .views import UserProfileUpdateView # <-- Isay import karein

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login-check/', login_check, name='login_check'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile-update'),
]
