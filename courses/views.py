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
            if user_answers.get(str(quiz.id)) == quiz.correct_answer:
                correct_count += 1

        score_percentage = (correct_count / total_questions) * 100

        # SmartEduX Rule: 80% marks for Certificate
        certificate_issued = False
        if score_percentage >= 80:
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

# --- FR-15: Student Dashboard API ---
class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Student ki enrollments nikalna
        enrollments = Enrollment.objects.filter(student=request.user)
        enrolled_courses = [e.course.title for e in enrollments]

        # 2. Student ke certificates nikalna
        certs = Certificate.objects.filter(student=request.user)
        earned_certificates = []
        for c in certs:
            earned_certificates.append({
                "course": c.course.title,
                "score": c.score,
                "date": c.issued_at.strftime("%Y-%m-%d")
            })

        # 3. Final data bhejien
        return Response({
            "user": request.user.username,
            "enrolled_in": enrolled_courses,
            "my_certificates": earned_certificates,
            "total_achievements": len(earned_certificates)
        })
    
class TeacherDashboardListView(APIView):
    """
    Teacher apne saare banaye huaye courses dekh sakta hai
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Validation: Check ke user waqai teacher hai ya nahi
        if request.user.role != 'teacher':
            return Response({"error": "Access denied. Only teachers can view this dashboard."}, status=status.HTTP_403_FORBIDDEN)
        
        # Sirf is login teacher ke courses fetch karein
        courses = Course.objects.filter(instructor=request.user)
        
        # Simple list serialize kar rahe hain bina naye serializer ke hassle ke
        course_list = []
        for course in courses:
            course_list.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "created_at": course.created_at if hasattr(course, 'created_at') else None
            })
            
        return Response({
            "teacher_name": request.user.username,
            "total_courses": courses.count(),
            "courses": course_list
        }, status=status.HTTP_200_OK)


class TeacherEnrolledStudentsView(APIView):
    """
    Diagram ke mutabiq: 'View Enrolled Students' feature.
    Teacher dekh sakta hai ke uske makhsoos course mein kaun kaun se students enrolled hain.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        if request.user.role != 'teacher':
            return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Check karein ke yeh course isi teacher ka hai ya nahi
            course = Course.objects.get(id=course_id, instructor=request.user)
        except Course.DoesNotExist:
            return Response({"error": "Course not found or you are not the instructor of this course."}, status=status.HTTP_404_NOT_FOUND)
        
        # Is course ki tamam enrollments nikalien
        enrollments = Enrollment.objects.filter(course=course)
        
        student_list = []
        for enroll in enrollments:
            student_list.append({
                "student_id": enroll.student.id,
                "student_name": enroll.student.username,
                "student_email": enroll.student.email,
                "enrolled_at": enroll.enrolled_at if hasattr(enroll, 'enrolled_at') else None
            })
            
        return Response({
            "course_title": course.title,
            "total_enrolled_students": enrollments.count(),
            "students": student_list
        }, status=status.HTTP_200_OK)