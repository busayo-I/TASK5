# video_project/urls.py
from django.urls import path
from link.views import CreateVideo, AddVideoData, CompleteVideo, StreamVideo

urlpatterns = [
    path('create/', CreateVideo.as_view(), name='create_video'),
    path('add_data/<int:video_id>/', AddVideoData.as_view(), name='add_video_data'),
    path('complete/<int:video_id>/', CompleteVideo.as_view(), name='complete_video'),
    path('stream/<int:video_id>/', StreamVideo.as_view(), name='stream_video'),
]
