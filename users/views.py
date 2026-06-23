from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate
import json
from rest_framework_simplejwt.tokens import RefreshToken  # Token generate karne ke liye

User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Validation
            if not data.get("username") or not data.get("password"):
                return JsonResponse({"error": "Username and password are required"}, status=400)

            # User Creation
            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                role=data.get("role", "student"),
                qualification=data.get("qualification"),
                experience_years=data.get("experience_years", 0),
            )
            
            return JsonResponse({
                "message": "User created successfully", 
                "user": user.username,
                "role": user.role
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def login_check(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            # User authenticate karna
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Agar user approved nahi hai (Teachers ke liye admin approval lazmi hai)
                if not user.is_approved:
                    return JsonResponse({"error": "Your account is pending admin approval."}, status=403)

                # Asli JWT Tokens generate karna
                refresh = RefreshToken.for_user(user)
                
                return JsonResponse({
                    "message": "Login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": user.username,
                    "role": user.role,
                    "is_approved": user.is_approved
                }, status=200)
                
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST allowed"}, status=405)


# Django REST Framework Views for Profile (Baari baari baki team ke kaam ke sath sync ho jayega)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user