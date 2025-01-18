from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.title

class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password_changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password changed for {self.user.username} on {self.password_changed_at}"
    
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    profile_picture = models.FileField(upload_to='profile_pictures/')