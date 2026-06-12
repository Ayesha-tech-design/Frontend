import os
import json
import re
import yt_dlp
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai  # Standard Google GenAI SDK
from .models import VideoNote

# =====================================================================
# PRODUCTION API INITIALIZATION
# =====================================================================
RAW_KEY = getattr(settings, "GEMINI_API_KEY", None)
CLEAN_KEY = str(RAW_KEY).replace("..key", "").strip() if RAW_KEY else None

print("\n[SMARTEDUX LOG 1]: Initializing Production GenAI Client...")
client = None
if CLEAN_KEY:
    client = genai.Client(api_key=CLEAN_KEY)
    print("-> SUCCESS: GenAI Client initialized seamlessly.")
else:
    print("-> WARNING: API Key missing or incorrect in settings.py.")


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
# MAIN API ENDPOINT
# =====================================================================
@api_view(['POST'])
def generate_notes(request):
    try:
        youtube_url = request.data.get('youtube_url', '')
        print("\n[SMARTEDUX LOG 2]: New Inbound Request.")
        print(f"-> Target URL: {youtube_url}")

        if not youtube_url:
            return Response({"status": "failed", "error": "YouTube URL required"}, status=400)

        # Extract Video ID
        if "v=" in youtube_url:
            video_id = youtube_url.split("v=")[1].split("&")[0]
        else:
            video_id = youtube_url.rstrip("/").split("/")[-1]

        print(f"-> Parsed Video ID: {video_id}")

        # Database Check (Checking via video_url since it is in our model)
        existing = VideoNote.objects.filter(video_url=youtube_url).first()
        if existing:
            print("\n[SMARTEDUX LOG 3]: PostgreSQL Cache Hit. Returning stored content.")
            return Response({
                "status": "success",
                "source": "database",
                "summary": existing.summary,
                "quiz": []  # Safely returning empty array if field not in models
            })

        # Content Extraction
        raw_text = ""
        is_transcript_available = True

        print("\n[SMARTEDUX LOG 4]: Pulling content from YouTube source...")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
            raw_text = " ".join([item['text'] for item in transcript])
            print("-> Success: Transcript pulled cleanly.")
        except Exception as tx_err:
            print(f"-> Transcript API offline ({str(tx_err)}). Scraping via fallback layer...")
            is_transcript_available = False
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(youtube_url, download=False)
                    video_title = info.get('title', '')
                    video_desc = info.get('description', '')[:500]
                    raw_text = f"Title: {video_title}\nDescription: {video_desc}"
                print("-> Success: Metadata scraped via yt-dlp.")
            except Exception as ytdlp_err:
                print(f"-> Critical Scraping Failure: {str(ytdlp_err)}")
                raw_text = "Educational Topic Content"

        raw_text = raw_text[:3000]

        # Active AI Request Generation Layer
        try:
            print("\n[SMARTEDUX LOG 5]: Directing payload to GenAI Client Engine...")
            if not client:
                raise Exception("GenAI Client was not initialized properly.")

            prompt = f"""
You are an academic assistant built into the SmartEduX e-learning platform.
Analyze the provided context and return a strict raw JSON object.

RULES:
- Return ONLY a valid, parseable JSON structure.
- Do NOT include markdown code blocks like ```json or wrappers.
- Do NOT include any conversational introduction or summary text.

STRUCTURE:
{{
  "summary": "Detailed educational notes formatted nicely in clear bullet points.",
  "quiz": [
    {{
      "question": "A conceptual academic question from the text?",
      "options": {{
        "A": "First Choice",
        "B": "Second Choice",
        "C": "Third Choice",
        "D": "Fourth Choice"
      }},
      "answer": "A"
    }}
  ]
}}

Generate exactly 5 high-quality academic MCQs inside the quiz array.

Context Text:
{raw_text}
"""
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            print("[SMARTEDUX LOG 6]: Clean GenAI Response Secured.")
            
            ai_text = response.text.strip()
            json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            clean_json = json_match.group() if json_match else ai_text

            data = json.loads(clean_json, strict=False)
            print("-> Success: Decoded into accurate active JSON fields.")
            source_type = "gemini_transcript" if is_transcript_available else "gemini_title_fallback"

        except Exception as gemini_err:
            print("\n[SMARTEDUX LOG 7]: GenAI Client Engine Failure.")
            print(f"-> Diagnostic Details: {str(gemini_err)}")
            data = local_summary_generator(raw_text)
            source_type = "fallback"

        # Database Commit matched with notes/models.py fields
        print("\n[SMARTEDUX LOG 8]: Syncing structured dataset to PostgreSQL...")
        VideoNote.objects.create(
            video_title=video_id,  # Using video_id as fallback title for entry
            video_url=youtube_url,
            transcript=raw_text,
            summary=data.get("summary", "")
        )
        print("-> Database Sync Complete.")

        return Response({
            "status": "success",
            "source": source_type,
            "summary": data.get("summary", ""),
            "quiz": data.get("quiz", [])
        })

    except Exception as api_fatal_err:
        print(f"\n[CRITICAL API FAULT]: {str(api_fatal_err)}")
        return Response({"status": "failed", "error": str(api_fatal_err)}, status=500)