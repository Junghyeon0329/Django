from django.db import models
from django.contrib.auth.models import User
    
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "notice"
        
    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    profile_picture = models.FileField(upload_to='profile_pictures/')
