from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from .utils import fetch_and_download_videos
from .tasks import fetch_and_download_videos
# from .serializers import VideoSerializer
# from .models import Video

@api_view(["GET"])
def fetch_videos_api(request):
    try:
        # Fetch and download new videos
        fetch_and_download_videos.delay()  # Background execution
        
        # Optionally filter or sort videos (e.g., latest 10)
        # recent_videos = Video.objects.order_by("-published_at")[:10]
        # serialized = VideoSerializer(recent_videos, many=True)

        return Response({
            "message": "Videos fetched and downloaded successfully.",
            # "videos": serialized.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
