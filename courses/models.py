from django.db import models
from django.conf import settings

# FR-4: Course Management (Instructor)
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='courses_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title

# FR-5: Course Enrollment (Student)
class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='enrolled_students'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Business Rule: Duplicate enrollment must be prevented
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    # FR-13 & FR-14: Quiz aur Certification Logic
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"Quiz for {self.course.title}"

class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    is_passed = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Business Rule: Passing criteria is 80% or above
        if self.score >= 80:
            self.is_passed = True
        else:
            self.is_passed = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate for {self.student.username} - {self.course.title}"