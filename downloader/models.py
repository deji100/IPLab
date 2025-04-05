from django.db import models


class Channel(models.Model):
    channel_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Video(models.Model):
    video_id = models.CharField(max_length=100, unique=True)  # YouTube video ID
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, default=1, related_name='videos')
    thumbnail_default = models.URLField(blank=True)
    thumbnail_medium = models.URLField(blank=True)
    thumbnail_high = models.URLField(blank=True)
    published_at = models.DateTimeField()
    local_path = models.FileField(upload_to="videos/", blank=True, null=True)  # Optional until downloaded

    def __str__(self):
        return self.title
