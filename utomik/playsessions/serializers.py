from rest_framework import serializers
from .models import PlaySession

class PlaySessionSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(read_only=True)

    class Meta:
        model = PlaySession
        fields = ('user', 'game', 'time_started', 'time_ended', 'duration')
