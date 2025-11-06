from django.db import models
from cloudinary.models import CloudinaryField

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    poster = CloudinaryField('image', blank=True, null=True)
    # poster = models.ImageField(upload_to='events/', blank=True)
    tags = models.JSONField(default=list)  # ["sports", "tech"]

    def __str__(self):
        return self.title
