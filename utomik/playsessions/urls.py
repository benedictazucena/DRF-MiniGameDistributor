from django.urls import path
from .views import PlaySessionView

app_name = 'playsessions'

urlpatterns = [
    path('', PlaySessionView.as_view(), name='playsession'),
    path('<int:pk>/', PlaySessionView.as_view(), name='playsession_detail'),
    path('game/<int:game_id>/', PlaySessionView.as_view(), name='playsession_game'),
    path('user/<int:user_id>/', PlaySessionView.as_view(), name='playsession_user'),
]
