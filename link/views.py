from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video, VideoChunk
from .serializer import VideoSerializer
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os
from django.http import StreamingHttpResponse, FileResponse
from django.shortcuts import get_object_or_404

class Status(APIView):
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    
class CreateVideoList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, requst: Request):
        data = requst.data()
        video = data.get("video")
        title = data.get("title")
        description = data.get("description")

        if video is None:
            response = {
                "Status": "Error",
                "Massage": "Video file is required.",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            video_obj = serializer.save()
            video_url = 
            video_obj.video_url = video_url
            video_obj.save()

            try:
                chunk_directory = os.path.join(settings.MEDIA_ROOT, 'video_chunks', str(video_obj.id))
                os.makedirs(chunk_directory, exist_ok=True)
                chunk_number = 0

                while True:
                    chunk = video.read(1024 * 1024)

                    if chunk is None:
                        break

                    chunk_filename = f"chunk_{chunk_number}.mp4"
                    chunk_path = os.path.join(chunk_directory, chunk_filename)

                    with open(chunk_path, "wb") as chunk_file:
                        chunk_file.write(chunk)
                    #creating a video chunk object
                    video_chunk = VideoChunk.objects.create(
                        video=video_obj,
                        chunk_number=chunk_number,
                        chunk_file=chunk_path
                    )
                    video_chunk.save()
                    chunk_number = chunk_number + 1
            except Exception as e:
                response = {
                    "Status": "Error",
                    "Massage": "Error while uploading video chunks.",
                    "data": str(e)
                }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response = {
                "Status": "Success",
                "Massage": "Video uploaded successfully.",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "Status": "Error",
                    "Massage": "Video not created.",
                    "data": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        


# class VideoViewSet(viewsets.ModelViewSet):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.date) 
