from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import responses
from .models import Video
from .serializer import VideoSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):