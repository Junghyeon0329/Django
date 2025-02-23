from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PasswordHistory(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pw_changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "operation_pw_changed"

    def __str__(self):
        return f"Password changed for {self.user.username} on {self.pw_changed_at}"
    