from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.name
