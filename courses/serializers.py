from rest_framework import serializers
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
        read_only_fields = ['student', 'enrolled_at'] # Student login se khud uthayenge
from .models import Quiz, Certificate

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'course', 'score', 'is_passed', 'issued_at']