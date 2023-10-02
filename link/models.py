from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # processing_status = models.CharField(
    #     max_length=20,
    #     choices=(
    #         ('processing', 'Processing'),
    #         ('completed', 'Completed'),
    #         ('failed', 'Failed'),
    #     ),
    #     default='processing'
    PROCESSING_IN_PROGRESS = 'in_progress'
    PROCESSING_COMPLETED = 'completed'
    PROCESSING_FAILED = 'failed'

    # Add a field to store the processing status
    processing_status = models.CharField(
        max_length=20,
        default=PROCESSING_IN_PROGRESS,  # Set the default status as in progress
        choices=(
            (PROCESSING_IN_PROGRESS, 'Processing In Progress'),
            (PROCESSING_COMPLETED, 'Processing Completed'),
            (PROCESSING_FAILED, 'Processing Failed'),
        )
    )
    

    def __str__(self):
        return self.title

class VideoChunk(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    chunk_number = models.PositiveIntegerField()
    chunk_file = models.FileField(upload_to='video_chunks/')

    def __str__(self):
        return f"Chunk {self.chunk_number} of {self.video.title}"
