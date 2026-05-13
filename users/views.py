from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import json

User = get_user_model()

#Signup
@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Check karein ke zaroori cheezein maujood hain
            if not data.get("username") or not data.get("password"):
                return JsonResponse({"error": "Username and password are required"}, status=400)

            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                role=data.get("role", "student"), # Default student
                qualification=data.get("qualification"),
                experience_years=data.get("experience_years", 0),
            )
            return JsonResponse({"message": "User created successfully", "user": user.username}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST allowed"}, status=405)
#  LOGIN 
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if user:
            return JsonResponse({
                "message": "Login successful",
                "user": user.username,
                "role": user.role
            })

        return JsonResponse({"error": "Invalid credentials"})

    return JsonResponse({"error": "Only POST allowed"})