from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video, VideoChunk
from .serializer import VideoSerializer
from rest_framework.request import Request
from django.conf import settings
import os
from django.http import StreamingHttpResponse, FileResponse
from django.shortcuts import get_object_or_404

class CreateVideo(APIView):
    def post(self, request: Request):
        serializer = VideoSerializer(data={})
        if serializer.is_valid():
            video_obj = serializer.save()
            response = {
                "status": "success",
                "message": "Video created successfully",
                "video_id": video_obj.id
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status": "error",
                "message": "Video not created",
                "data": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class AddVideoChunk(APIView):
    def post(self, request: Request, video_id):
        video_chunk = request.data.get('video_chunk')
        chunk_number = request.data.get('chunk_number')

        if not video_chunk or chunk_number is None:
            response = {
                "status": "error",
                "message": "Video chunk and chunk number are required.",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            video_obj = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"status": "error", "message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            chunk_directory = os.path.join(settings.MEDIA_ROOT, 'video_chunks', str(video_id))
            os.makedirs(chunk_directory, exist_ok=True)
            chunk_filename = f'chunk_{chunk_number}.mp4'
            chunk_path = os.path.join(chunk_directory, chunk_filename)

            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(video_chunk.read())

            # Create a VideoChunk object for this chunk
            video_chunk = VideoChunk.objects.create(
                video=video_obj,
                chunk_number=chunk_number,
                chunk_file=chunk_path
            )
            video_chunk.save()

            response = {
                "status": "success",
                "message": "Video chunk uploaded successfully",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "status": "error",
                "message": "Error uploading video chunk.",
                "data": str(e)
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompleteVideo(APIView):
    def post(self, request: Request, video_id):
        try:
            video_obj = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"status": "error", "message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        response_message = "Video marked as complete"
        video_obj.completed = True
        video_obj.save()

        response = {
            "status": "success",
            "message": response_message,
        }
        return Response(response, status=status.HTTP_200_OK)

class StreamVideo(APIView):
    def get(self, request: Request, video_id):
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"status": "error", "message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        chunk_files = VideoChunk.objects.filter(video=video).order_by('chunk_number')

        def generate_chunks():
            for chunk_file in chunk_files:
                with open(chunk_file.chunk_file.path, 'rb') as file:
                    for chunk in file:
                        yield chunk

        response = StreamingHttpResponse(generate_chunks(), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
        return response