from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Item(models.Model):
    TYPE = [('lost', 'Lost'), ('found', 'Found')]
    title = models.CharField(max_length=200)
    description = models.TextField()
    # image = models.ImageField(upload_to='lostfound/', blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    type = models.CharField(max_length=5, choices=TYPE)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    claimed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.type}: {self.title}"

class Chat(models.Model):
    messages = models.JSONField(default=list)
