from django.urls import path
from . import views

urlpatterns = [
    path('create_video/', views.CreateVideo.as_view(), name='create_video'),
    path('add_video_chunk/<int:video_id>/', views.AddVideoChunk.as_view(), name='add_video_chunk'),
    path('complete_video/<int:video_id>/', views.CompleteVideo.as_view(), name='complete_video'),
    path('stream_video/<int:video_id>/', views.StreamVideo.as_view(), name='stream_video'),
]