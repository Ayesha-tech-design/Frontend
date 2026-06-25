from django.db import models
from django.conf import settings
from courses.models import Course  # Taake notes course se link hon
from django.contrib.auth.models import User

# 1. Ayesha ka Note Model
class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()  # AI generated summary yahan save hogi
    video_url = models.URLField(blank=True, null=True)  # Source video
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 2. Zunaira ka VideoNote Model (Indentation Fixed)
class VideoNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_notes', null=True, blank=True)
    video_title = models.CharField(max_length=255)
    video_url = models.URLField()
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_title