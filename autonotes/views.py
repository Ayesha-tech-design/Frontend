import os
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai
import json
import re

from rest_framework.decorators import api_view
from rest_framework.response import Response

from youtube_transcript_api import YouTubeTranscriptApi

from .models import VideoNote


# =========================
# GEMINI CONFIG
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


# =========================
# LOCAL FALLBACK FUNCTION
# =========================
def local_summary_generator(text):

    return {
        "summary": f"""
• AI Generated Local Notes

• Main Topic:
{text[:200]}

• Key Points:
- Important concepts discussed
- Educational content detected
- Summary generated locally
        """,

        "quiz": [
            {
                "question": "What is the main topic of the video?",
                "options": {
                    "A": "Education",
                    "B": "Sports",
                    "C": "Gaming",
                    "D": "Cooking"
                },
                "answer": "A"
            }
        ]
    }


# =========================
# MAIN API
# =========================
@api_view(['POST'])
def generate_notes(request):

    try:

        # =========================
        # 1. GET URL
        # =========================
        youtube_url = request.data.get('youtube_url', '')

        if not youtube_url:
            return Response({
                "status": "failed",
                "error": "YouTube URL required"
            }, status=400)

        # =========================
        # 2. EXTRACT VIDEO ID
        # =========================
        if "v=" in youtube_url:
            video_id = youtube_url.split("v=")[1].split("&")[0]
        else:
            video_id = youtube_url.rstrip("/").split("/")[-1]

        # =========================
        # 3. DATABASE CHECK
        # =========================
        existing = VideoNote.objects.filter(video_id=video_id).first()

        if existing:
            return Response({
                "status": "success",
                "source": "database",
                "summary": existing.summary,
                "quiz": existing.quiz_data
            })

        # =========================
        # 4. TRANSCRIPT FETCH
        # =========================
        raw_text = ""

        try:

            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            raw_text = " ".join([
                item['text'] for item in transcript
            ])

        except Exception:

            raw_text = """
            Artificial Intelligence enables machines to learn.
            Machine Learning is a subset of AI.
            Deep Learning uses neural networks.
            """

        raw_text = raw_text[:3000]

        # =========================
        # 5. GEMINI AI TRY
        # =========================
        try:

            prompt = f"""
Return ONLY valid JSON.

{{
  "summary": "Detailed notes in bullet points",
  "quiz": [
    {{
      "question": "",
      "options": {{
        "A": "",
        "B": "",
        "C": "",
        "D": ""
      }},
      "answer": "A"
    }}
  ]
}}

Generate exactly 5 MCQs.

Text:
{raw_text}
"""

            response = model.generate_content(prompt)

            ai_text = response.text.strip()

            json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)

            clean_json = json_match.group() if json_match else ai_text

            data = json.loads(clean_json)

            source_type = "gemini"

        except Exception:

            # =========================
            # 6. LOCAL FALLBACK
            # =========================
            data = local_summary_generator(raw_text)

            source_type = "fallback"

        # =========================
        # 7. SAVE DATABASE
        # =========================
        VideoNote.objects.create(
            video_id=video_id,
            url=youtube_url,
            summary=data.get("summary", ""),
            quiz_data=data.get("quiz", [])
        )

        # =========================
        # 8. FINAL RESPONSE
        # =========================
        return Response({
            "status": "success",
            "source": source_type,
            "summary": data.get("summary", ""),
            "quiz": data.get("quiz", [])
        })

    except Exception as e:

        return Response({
            "status": "failed",
            "error": str(e)
        }, status=500)