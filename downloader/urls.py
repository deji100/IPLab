from django.urls import path
from .views import fetch_videos_api

urlpatterns = [
    path('api/fetch-videos/', fetch_videos_api, name='fetch_videos_api'),
]
