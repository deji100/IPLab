from django.contrib import admin
from .models import Video, Channel

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "video_id", "channel", "published_at")
    search_fields = ("title", "video_id", "channel__title")
    list_filter = ("published_at", "channel")

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("title", "channel_id")
    search_fields = ("title", "channel_id")
