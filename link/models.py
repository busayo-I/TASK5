from django.db import models

# Create your models here.
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    Video_file = models.FileField(upload_to='Video/')
    upload_data = models.DateTimeField(auto_now_add=True)

class VideoChunk(models.Model):
    video = models.ForeignKey('Video', related_name='chunks', on_delete=models.CASCADE)
    chunk_number = models.PositiveBigIntegerField()
    chunk_file = models.FileField(upload_to='video_chunks/')


    def __str__(self):
        return self.title
        return f'Chunk {self.chunk_number} of {self.video.title}'
