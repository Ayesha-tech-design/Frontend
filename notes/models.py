from django.db import models
from django.conf import settings
from courses.models import Course # Taake notes course se link hon

class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField() # AI generated summary yahan save hogi
    video_url = models.URLField(blank=True, null=True) # Source video
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title