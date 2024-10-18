from django.db import models

class Role(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    permissions = models.ManyToManyField(
        "permissions.Permission",
        related_name="roles",
    )
    users = models.ManyToManyField(
        "users.User",
        related_name="roles",
    )

    class Meta:
        db_table = "role"

    def __str__(self):
        return f"Role#{self.id}:{self.name}"
