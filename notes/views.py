import os
import json
import re
import yt_dlp
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from .models import VideoNote

# === AUTHENTICATION IMPORTS (Zunaira ka Core Task) ===
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# PRODUCTION API INITIALIZATION
RAW_KEY = getattr(settings, "GEMINI_API_KEY", None)
CLEAN_KEY = str(RAW_KEY).replace("..key", "").strip() if RAW_KEY else None

client = genai.Client(api_key=CLEAN_KEY) if CLEAN_KEY else None


def local_summary_generator(text):
    return {
        "summary": f"• AI Generated Local Notes\n\n• Main Topic:\n{text[:300]}\n\n• Key Points:\n- Educational concepts detected\n- Generated via local structure backup.",
        "quiz": [
            {
                "question": "What is the primary subject discussed?",
                "options": {"A": "Academic Topic", "B": "Entertainment", "C": "Gaming", "D": "Cooking"},
                "answer": "A"
            }
        ]
    }


# =====================================================================
# MAIN API ENDPOINT (Notes & Quiz Generation - FIXED FOR LIVE LINKS)
# =====================================================================
@api_view(['POST'])
def generate_notes(request):
    try:
        # 1. Live Input Extraction from Frontend
        youtube_url = request.data.get('youtube_url', '').strip()
        print(f"\n[SMARTEDUX LIVE LOG]: Incoming Link from Frontend: {youtube_url}")

        if not youtube_url:
            return Response({"status": "failed", "error": "YouTube URL required"}, status=400)

        # 2. Advanced Video ID Parser (Har format handle karega)
        video_id = ""
        if "v=" in youtube_url:
            video_id = youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
        else:
            video_id = youtube_url.rstrip("/").split("/")[-1]

        print(f"-> Parsed Unique Video ID: {video_id}")

        if not video_id:
            return Response({"status": "failed", "error": "Invalid YouTube URL format"}, status=400)

        # 3. PUKKA CACHE CHECK VIA VIDEO ID
        existing = VideoNote.objects.filter(video_title=video_id).first()
        if existing:
            print("-> Database Cache Hit: Returning pre-existing records instantly.")
            return Response({
                "status": "success",
                "source": "database",
                "summary": existing.summary,
                "quiz": []
            })

        # 4. Fresh Content Extraction Loop
        raw_text = ""
        is_transcript_available = True
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
            raw_text = " ".join([item['text'] for item in transcript])
            source_type = "gemini_transcript"
        except Exception:
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(youtube_url, download=False)
                    raw_text = f"Title: {info.get('title', '')}\nDescription: {info.get('description', '')[:500]}"
                source_type = "gemini_metadata_fallback"
            except Exception:
                raw_text = "Standard Educational Domain Video Content Text"
                source_type = "fallback"

        raw_text = raw_text[:3000]

        # 5. Live GenAI Content Production
        prompt = f"""
        You are an academic assistant built into the SmartEduX platform.
        Analyze the provided context and return a strict raw JSON object.
        Generate exactly 5 high-quality academic MCQs inside the quiz array.

        STRUCTURE:
        {{
          "summary": "Detailed educational notes formatted nicely in clear bullet points.",
          "quiz": [
            {{
              "question": "Question text?",
              "options": {{"A": "Choice 1", "B": "Choice 2", "C": "Choice 3", "D": "Choice 4"}},
              "answer": "A"
            }}
          ]
        }}

        Context Text:
        {raw_text}
        """
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        
        ai_text = response.text.strip()
        json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
        clean_json = json_match.group() if json_match else ai_text
        data = json.loads(clean_json, strict=False)

        # 6. Database Entry Lock (Unique entry save karna)
        VideoNote.objects.create(
            video_title=video_id,  # Locking Identity
            video_url=youtube_url,
            transcript=raw_text,
            summary=data.get("summary", "")
        )
        print("-> Database Sync Complete for new video.")

        return Response({
            "status": "success",
            "source": source_type,
            "summary": data.get("summary", ""),
            "quiz": data.get("quiz", [])
        })

    except Exception as err:
        return Response({"status": "failed", "error": str(err)}, status=500)


# =====================================================================
# USER AUTHENTICATION ENDPOINTS (Zunaira's Core Tasks)
# =====================================================================

@api_view(['POST'])
def register_user(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"status": "failed", "error": "All fields required"}, status=400)

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            return Response({"status": "failed", "error": "User already registered"}, status=400)

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        return Response({"status": "success", "message": "Registered successfully!"}, status=201)
    except Exception as err:
        return Response({"status": "failed", "error": str(err)}, status=500)


@api_view(['POST'])
def login_user(request):
    try:
        email_or_username = request.data.get('email')
        password = request.data.get('password')

        if not email_or_username or not password:
            return Response({"status": "failed", "error": "All fields required"}, status=400)

        target_username = email_or_username
        if "@" in email_or_username:
            user_obj = User.objects.filter(email=email_or_username).first()
            if user_obj: 
                target_username = user_obj.username

        user = authenticate(username=target_username, password=password)
        if user is not None:
            login(request, user)
            return Response({"status": "success", "message": "Login successful!"}, status=200)
        return Response({"status": "failed", "error": "Invalid credentials"}, status=401)
    except Exception as err:
        return Response({"status": "failed", "error": str(err)}, status=500)
    # =====================================================================
# HISTORY MANAGEMENT MODULE (Ayesha's Dashboard Storage & Fetch)
# =====================================================================
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Yeh check karega ke valid JWT token header mein hai ya nahi
def save_history(request):
    try:
        # Django REST framework ke mutabik request.data use kiya hai form/JSON body ke liye
        title = request.data.get('video_title')
        url = request.data.get('video_url')
        transcript_text = request.data.get('transcript')
        summary_text = request.data.get('summary')
        
        if not title or not url:
            return Response({"status": "failed", "error": "Video title and URL are required"}, status=400)

        # Database object lock karna current authorized user ke sath
        history_item = VideoNote.objects.create(
            user=request.user,  # Custom profile/user request se automatic fetch ho jayega
            video_title=title,
            video_url=url,
            transcript=transcript_text,
            summary=summary_text
        )
        
        print(f"\n[SMARTEDUX STORAGE LOG]: New history node successfully synced for: {request.user.username}")
        return Response({"status": "success", "message": "History saved successfully!"}, status=201)
        
    except Exception as err:
        return Response({"status": "failed", "error": str(err)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_history(request):
    try:
        # Sirf current request.user ka data reverse chronological order (-created_at) mein filter karna
        user_history = VideoNote.objects.filter(user=request.user).order_by('-created_at')
        
        # Data objects ko automatic array/list format mein convert karna frontend response ke liye
        history_list = []
        for item in user_history:
            history_list.append({
                "id": item.id,
                "video_title": item.video_title,
                "video_url": item.video_url,
                "summary": item.summary,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M")
            })
            
        return Response({
            "status": "success",
            "total_records": len(history_list),
            "history": history_list
        }, status=200)
        
    except Exception as err:
        return Response({"status": "failed", "error": str(err)}, status=500)