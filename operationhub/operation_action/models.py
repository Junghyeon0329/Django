from django.db import models
from django.contrib.auth.models import User
    
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    profile_picture = models.FileField(upload_to='profile_pictures/')
        
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    receiver_email = models.EmailField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver_email}: {self.text}"

    class Meta:
        ordering = ['timestamp']