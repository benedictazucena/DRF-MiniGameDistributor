# views.py
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer

class GameListCreateView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class GameRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        game = self.get_object()
        game.delete()
        return Response(status=204)
