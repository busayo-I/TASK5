from django.db import models

# Create your models here.
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    Video_file = models.FileField(upload_to='Video/')
    upload_data = models.DateTimeField(auto_now_add=True)