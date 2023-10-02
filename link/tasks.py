# video_app/tasks.py
from celery import shared_task
from .models import Video, VideoChunk
from subprocess import run, PIPE
import os

@shared_task
def process_video(video_id):
    try:
        video = Video.objects.get(pk=video_id)

        # Define the directory where video chunks are stored
        chunk_directory = os.path.join('media', 'video_chunks', str(video_id))

        # Get a list of video chunk file paths
        chunk_files = [os.path.join(chunk_directory, f'chunk_{i}.mp4') for i in range(video.videochunk_set.count())]

        # Combine video chunks into a single video file
        output_file = os.path.join(chunk_directory, 'combined_video.mp4')
        cmd = [
            'ffmpeg',
            '-i', f'concat:{"|".join(chunk_files)}',
            '-c', 'copy',
            output_file
        ]
        run(cmd, stdout=PIPE, stderr=PIPE, text=True, check=True)

        # Perform video transcription using Whisper (replace with your transcription service)
        transcription_file = os.path.join(chunk_directory, 'transcription.txt')
        cmd = [
            'whisper-transcribe',
            '-i', output_file,
            '-o', transcription_file
        ]
        run(cmd, stdout=PIPE, stderr=PIPE, text=True, check=True)

        # Store the transcription file path in the video model
        video.transcription_file = transcription_file
        video.save()

    except Exception as e:
        # Handle any exceptions or errors during video processing
        video.transcription_file = None  # Set transcription file to None on error
        video.save()
