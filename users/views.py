from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import json

User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Validation
            if not data.get("username") or not data.get("password"):
                return JsonResponse({"error": "Username and password are required"}, status=400)

            # User Creation based on your models.py logic
            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                role=data.get("role", "student"),
                qualification=data.get("qualification"),
                experience_years=data.get("experience_years", 0),
            )
            
            # Note: models.py mein humne save() method likha hai jo students ko auto-approve kar dega
            return JsonResponse({
                "message": "User created successfully", 
                "user": user.username,
                "role": user.role
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST allowed"}, status=405)

# Tip: Manual login ki zaroorat nahi kyunke hum JWT use kar rahe hain, 
# lekin agar aap sirf check karne ke liye rakhna chahti hain toh ye version sahi hai.
@csrf_exempt
def login_check(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = authenticate(username=data["username"], password=data["password"])
            if user:
                return JsonResponse({
                    "message": "Credentials valid",
                    "user": user.username,
                    "role": user.role,
                    "is_approved": user.is_approved
                })
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST allowed"}, status=405)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ye login kiye huye user ka data return karega
        return self.request.user