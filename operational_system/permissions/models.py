from django.db import models

class Permission(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = "permission"

    def __str__(self):
        return f"Permission#{self.id}:{self.name}"

