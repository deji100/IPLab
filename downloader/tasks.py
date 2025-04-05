import yt_dlp
import requests
import re
from celery import shared_task
from downloader.models import Video, Channel
from django.utils.dateparse import parse_datetime


API_KEY = "AIzaSyAbj3OSHJdNoni-SAinDYt6c4AD2hv1tYg"
CHANNEL_ID = "UCOsQ3iGRosvnpP1hAdtplvQ"


def parse_duration(duration):
    match = re.match(r'PT(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0
    minutes = int(match.group(1)) if match.group(1) else 0
    seconds = int(match.group(2)) if match.group(2) else 0
    return minutes * 60 + seconds


@shared_task
def fetch_and_download_videos():
    search_url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet&type=video&maxResults=10"
    )
    search_response = requests.get(search_url).json()

    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]

        if Video.objects.filter(video_id=video_id).exists():
            continue

        details_url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?key={API_KEY}&id={video_id}&part=contentDetails"
        )
        details_response = requests.get(details_url).json()
        items = details_response.get("items", [])
        if not items:
            continue

        duration = items[0]["contentDetails"].get("duration", "")
        total_seconds = parse_duration(duration)

        if total_seconds <= 61:
            print(f"Skipping short video: {video_id} ({total_seconds}s)")
            continue

        channel_id = snippet["channelId"]
        channel_title = snippet["channelTitle"]
        channel, _ = Channel.objects.get_or_create(
            channel_id=channel_id,
            defaults={"title": channel_title}
        )

        ydl_opts = {
            "outtmpl": f"media/videos/{video_id}.mp4",
            "format": "bestvideo+bestaudio/best"
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        except Exception as e:
            print(f"Failed to download {video_id}: {e}")
            continue

        thumbnails = snippet.get("thumbnails", {})
        thumbnail_default = thumbnails.get("default", {}).get("url", "")
        thumbnail_medium = thumbnails.get("medium", {}).get("url", "")
        thumbnail_high = thumbnails.get("high", {}).get("url", "")

        Video.objects.create(
            title=snippet.get("title", ""),
            video_id=video_id,
            description=snippet.get("description", ""),
            thumbnail_default=thumbnail_default,
            thumbnail_medium=thumbnail_medium,
            thumbnail_high=thumbnail_high,
            local_path=f"videos/{video_id}.mp4",
            published_at=parse_datetime(snippet.get("publishedAt")),
            channel=channel
        )
