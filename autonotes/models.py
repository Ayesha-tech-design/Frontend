from django.db import models

class VideoNote(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    summary = models.TextField()
    quiz_data = models.JSONField()  # Ismein MCQs save honge
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_id