from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email_id = models.CharField(max_length=500)    
    password = models.CharField(max_length=500)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"User#{self.id}:{self.name}:{self.phone_number}:{self.email_id}"
