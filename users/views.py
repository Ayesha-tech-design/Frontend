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
        data = json.loads(request.body)

        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            role=data["role"],
            qualification=data.get("qualification"),
            experience_years=data.get("experience_years", 0),
        )

        return JsonResponse({
            "message": "User created successfully",
            "user": user.username
        })

    return JsonResponse({"error": "Only POST allowed"})
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