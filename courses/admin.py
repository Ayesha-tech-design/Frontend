from django.contrib import admin
from .models import Course, Enrollment, Quiz, Certificate 

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Quiz)
admin.site.register(Certificate)