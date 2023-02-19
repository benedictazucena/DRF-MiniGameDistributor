from django.db import models
from django.conf import settings

class PlaySession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey('myapp.Game', on_delete=models.CASCADE)
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(blank=True, null=True)

    def duration(self):
        if not self.time_ended:
            return None
        return (self.time_ended - self.time_started).total_seconds()    

    def __str__(self):
        return f"{self.user} playing {self.game}"

    class Meta:
        unique_together = ('user', 'game',)
