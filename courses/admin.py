from django.contrib import admin
from .models import Course, Enrollment, Quiz, Certificate, CourseModule, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'instructor')

admin.site.register(Enrollment)
admin.site.register(Quiz)
admin.site.register(Certificate)
admin.site.register(CourseModule)
admin.site.register(Lesson)