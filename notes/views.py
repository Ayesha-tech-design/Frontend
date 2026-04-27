from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def generate_notes(request):
    youtube_url = request.data.get('youtube_url')
    if not youtube_url:
        return Response({"error": "Bhai, YouTube link toh do!"}, status=400)
    return Response({
        "message": " Kitchen mein YouTube link successfully receive ho gaya hai.",
        "received_url": youtube_url
    })
