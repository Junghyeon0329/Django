from django.db import models


class User(models.Model):
    email_id = models.CharField(max_length=31)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"User#{self.id}:{self.email_id}"
