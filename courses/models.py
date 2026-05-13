from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_created')
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title