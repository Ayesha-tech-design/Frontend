from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import json

# Sab models aur serializers yahan import kar diye hain
from .models import Course, Enrollment, Quiz, Certificate
from .serializers import EnrollmentSerializer, QuizSerializer, CertificateSerializer

# --- FR-4: Course Creation (Instructor) ---
@csrf_exempt
def create_course(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            instructor_id = data.get("instructor", 1) 

            course = Course.objects.create(
                title=data['title'],
                description=data['description'],
                instructor_id=instructor_id 
            )
            return JsonResponse({"message": "Course created successfully", "course_id": course.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    courses = list(Course.objects.values())
    return JsonResponse(courses, safe=False)

# --- FR-5: Course Enrollment (Student) ---
class EnrollInCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course nahi mila"}, status=status.HTTP_404_NOT_FOUND)

        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response(
                {"message": "Aap pehle se is course mein enroll hain"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        enrollment = Enrollment.objects.create(student=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# --- FR-13 & FR-14: Quiz Submission & Certification Logic ---
class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user_answers = request.data.get('answers') # Format: {"1": "A", "2": "B"}
        if not user_answers:
            return Response({"error": "Answers provide karein"}, status=status.HTTP_400_BAD_REQUEST)

        quizzes = Quiz.objects.filter(course_id=course_id)
        total_questions = quizzes.count()
        
        if total_questions == 0:
            return Response({"error": "Is course ke liye koi quiz maujood nahi hai"}, status=404)

        correct_count = 0
        for quiz in quizzes:
            # Check karein ke user ka answer sahi hai ya nahi
            if user_answers.get(str(quiz.id)) == quiz.correct_answer:
                correct_count += 1

        # Percentage calculate karein
        score_percentage = (correct_count / total_questions) * 100

        # SmartEduX Rule: 80% marks for Certificate
        certificate_issued = False
        if score_percentage >= 80:
            # Record score and issue certificate
            certificate, created = Certificate.objects.update_or_create(
                student=request.user,
                course_id=course_id,
                defaults={'score': score_percentage}
            )
            certificate_issued = True

        return Response({
            "score": score_percentage,
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "certificate_issued": certificate_issued,
            "message": "Congratulations! You have earned a certificate." if certificate_issued else "Score is too low. Certificate not issued."
        })