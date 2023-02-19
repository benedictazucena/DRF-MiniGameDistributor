from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .models import PlaySession
from games.models import Game
from users.models import CustomUser
from .serializers import PlaySessionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class PlaySessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        game_id = request.data.get('game_id')
        start_time = datetime.now()
        user_id = request.user.id
        game = get_object_or_404(Game, id=game_id)
        user = get_object_or_404(CustomUser, id=user_id)
        play_session = PlaySession(user=user, game=game, start_time=start_time)
        play_session.save()
        serializer = PlaySessionSerializer(play_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk, format=None):
        play_session = get_object_or_404(PlaySession, pk=pk)
        play_session.end_time = datetime.now()
        play_session.save()
        serializer = PlaySessionSerializer(play_session)
        return Response(serializer.data)

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')
        game_id = request.query_params.get('game_id')
        if user_id:
            user = get_object_or_404(CustomUser, id=user_id)
            play_sessions = PlaySession.objects.filter(user=user)
        elif game_id:
            game = get_object_or_404(Game, id=game_id)
            play_sessions = PlaySession.objects.filter(game=game)
        else:
            play_sessions = PlaySession.objects.all()
        total_duration = 0
        for play_session in play_sessions:
            if play_session.end_time is not None:
                duration = play_session.end_time - play_session.start_time
                total_duration += duration.total_seconds()
        return Response({'total_duration': total_duration})
