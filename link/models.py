from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class VideoChunk(models.Model):
    video = models.ForeignKey(Video, related_name='chunks', on_delete=models.CASCADE)
    chunk_number = models.IntegerField()
    chunk_file = models.FileField(upload_to='video_chunks/')

    def __str__(self):
        return f"{self.video.title} - Chunk {self.chunk_number}"
