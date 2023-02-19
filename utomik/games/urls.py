from django.urls import path
from .views import GameListCreateView, GameRetrieveUpdateDestroyView

app_name = 'games'

urlpatterns = [
    path('games/', GameListCreateView.as_view(), name='game-list'),
    path('games/<uuid:uuid>/', GameRetrieveUpdateDestroyView.as_view(), name='game-detail'),
]
