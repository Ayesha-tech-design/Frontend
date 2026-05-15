from django.contrib import admin
from django.urls import path

from autonotes.views import generate_notes

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/notes/generate/', generate_notes),
]