import os
import django
import pika
import json
import subprocess  # For running shell commands

# Set the DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")  # Replace 'your_project' with your actual project name

# Initialize Django settings
django.setup()

# Import the Video model after Django settings are initialized
from link.models import Video  # Replace 'link' with the actual app name

def process_video(video_id):
    try:
        video = Video.objects.get(pk=video_id)
        
        input_video_path = os.path.join('media/uploads', f'input_video_{video_id}.mp4')
        output_video_path = os.path.join('media/processed', f'processed_video_{video_id}.mp4')

        
        # Example: Video processing command (replace with your actual video processing command)
        command = f'ffmpeg -i {input_video_path} -vf "scale=640:480" {output_video_path}'
        
        # Run the video processing command
        subprocess.run(command, shell=True, check=True)
        
        # Update the video processing status to 'completed'
        video.processing_status = 'completed'
        video.save()
        
        return f"Video processing for video {video_id} is complete."
    
    except Exception as e:
        return f"Error processing video {video_id}: {str(e)}"

# Rest of your script (callback function, message queue setup, etc.) remains the same
