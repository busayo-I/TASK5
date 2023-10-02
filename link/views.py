from django.http import StreamingHttpResponse
from django.http import FileResponse
from django.http import JsonResponse
from .models import Video, VideoChunk
from .serializer import VideoSerializer
from django.conf import settings
import os
import pika
import json
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class Status(APIView):
    def get(self, request):
        return JsonResponse({'status': 'ok'}, status=status.HTTP_200_OK)

class CreateVideo(APIView):
    def post(self, request: Request):
        try:
            # Create a new Video object in the database and return its ID
            video = Video()
            video.save()
            return JsonResponse({'video_id': video.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddVideoData(APIView):
    def post(self, request: Request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        video_chunk = request.data.get('video_chunk')
        chunk_number = request.data.get('chunk_number')

        if not video_chunk or chunk_number is None:
            response = {
                "status": "error",
                "message": "Video chunk and chunk number are required.",
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            chunk_directory = os.path.join(settings.MEDIA_ROOT, 'video_chunks', str(video_id))
            os.makedirs(chunk_directory, exist_ok=True)
            chunk_filename = f'chunk_{chunk_number}.mp4'
            chunk_path = os.path.join(chunk_directory, chunk_filename)

            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(video_chunk.read())

            # Create a VideoChunk object for this chunk
            video_chunk_obj = VideoChunk.objects.create(
                video=video,
                chunk_number=chunk_number,
                chunk_file=chunk_path
            )
            video_chunk_obj.save()

            response = {
                "status": "success",
                "message": "Video chunk uploaded successfully",
            }
            return JsonResponse(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                "status": "error",
                "message": "Error uploading video chunk.",
                "data": str(e)
            }
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompleteVideo(APIView):
    def post(self, request: Request, video_id):
        try:
            video = get_object_or_404(Video, pk=video_id)
            if video.processing_status == Video.PROCESSING_COMPLETED:
                response = {
                    "status": "error",
                    "message": "Video processing already completed.",
                }
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

            # Establish a connection to RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            # Define the queue for video processing tasks
            channel.queue_declare(queue='video_processing')

            # Send a message to the queue with video_id
            message = json.dumps({'video_id': video_id})
            channel.basic_publish(exchange='', routing_key='video_processing', body=message)

            connection.close()

            video.processing_status = Video.PROCESSING_IN_PROGRESS
            video.save()

            response = {
                "status": "success",
                "message": "Video processing initiated.",
            }
            return JsonResponse(response, status=status.HTTP_202_ACCEPTED)
        except Video.DoesNotExist:
            response = {
                "status": "error",
                "message": "Video not found.",
            }
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                "status": "error",
                "message": "Error initiating video processing.",
                "data": str(e)
            }
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StreamVideo(APIView):
    def get(self, request: Request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        chunk_files = VideoChunk.objects.filter(video=video).order_by('chunk_number')

        def generate_chunks():
            for chunk_file in chunk_files:
                with open(chunk_file.chunk_file.path, 'rb') as file:
                    for chunk in file:
                        yield chunk

        response = StreamingHttpResponse(generate_chunks(), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
        return response
