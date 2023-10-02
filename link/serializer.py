# video_app/serializers.py
from rest_framework import serializers
from .models import Video, VideoChunk

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class VideoChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoChunk
        fields = '__all__'
