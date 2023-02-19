from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.contrib.auth import get_user_model
from .models import PlaySession
from games.models import Game
from .serializers import PlaySessionSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_game(name="", uuid="", genre=""):
        if name != "" and uuid != "" and genre != "":
            return Game.objects.create(name=name, uuid=uuid, genre=genre)

    @staticmethod
    def create_user(username="", password=""):
        if username != "" and password != "":
            User = get_user_model()
            user = User.objects.create_user(username=username, password=password)
            return user

    def setUp(self):
        self.user = self.create_user(username="testuser", password="testpassword")
        self.game = self.create_game(name="Test Game", uuid="1234", genre="Action")
        self.playsession = PlaySession.objects.create(
            user=self.user,
            game=self.game,
            start_time="2022-02-22T12:30:00Z"
        )
        self.client.force_authenticate(user=self.user)


class PlaySessionTest(BaseViewTest):

    def test_create_playsession(self):
        url = reverse("playsession-list")
        data = {"game_id": self.game.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_end_playsession(self):
        url = reverse("playsession-end", kwargs={"pk": self.playsession.id})
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_total_duration_for_user(self):
        url = reverse("playsession-duration")
        data = {"user_id": self.user.id}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("total_duration" in response.data)

    def test_get_total_duration_for_game(self):
        url = reverse("playsession-duration")
        data = {"game_id": self.game.id}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("total_duration" in response.data)
