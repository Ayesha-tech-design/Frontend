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
    
from django.db import models
from django.conf import settings  # Agar User model link karna ho

# Aapka purana class Course(models.Model) yahan pehle se maujood hai...

class CourseModule(models.Model):
    SECTION_CHOICES = [
        ('basic', 'Basic (Free)'),
        ('intermediate', 'Intermediate (Paid)'),
        ('advance', 'Advance (Paid)'),
    ]
    
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=255) # e.g., "Introduction to Python" ya "OOP Concepts"
    section_type = models.CharField(max_length=20, choices=SECTION_CHOICES, default='basic')
    sequence = models.IntegerField(default=1) # Sections ki tarteeb ke liye (1, 2, 3)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.course.title} - {self.get_section_type_display()} - {self.name}"


class Lesson(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255) # e.g., "What are Variables"
    
    # Hum dono options rakh rahe hain: direct video file ya phir YouTube/Cloudinary link
    video_url = models.URLField(blank=True, null=True) 
    video_file = models.FileField(upload_to='course_videos/', blank=True, null=True)
    
    sequence = models.IntegerField(default=1) # Modules ke andar videos ki tarteeb (Video 1, Video 2...)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.module.name} - Lesson: {self.title}"

        # =====================================================================
# ZUNAIRA'S ASSIGNMENT MANAGEMENT MODULE (100% FINAL CODE)
# =====================================================================
class AssignmentSubmission(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=255, default="Project Assignment")
    submission_file = models.FileField(upload_to='assignments_submitted/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.title}"