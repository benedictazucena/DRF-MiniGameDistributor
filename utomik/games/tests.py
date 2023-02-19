from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Game

class GameTests(APITestCase):
    def setUp(self):
        self.game = Game.objects.create(name='Test Game', uuid='123e4567-e89b-12d3-a456-426655440000', genre='Action')

    def test_create_game(self):
        url = reverse('game-list')
        data = {'name': 'New Game', 'uuid': '123e4567-e89b-12d3-a456-426655441111', 'genre': 'Adventure'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 2)
        self.assertEqual(Game.objects.get(uuid=data['uuid']).name, data['name'])

    def test_retrieve_game(self):
        url = reverse('game-detail', args=[str(self.game.uuid)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.game.name)

    def test_update_game(self):
        url = reverse('game-detail', args=[str(self.game.uuid)])
        data = {'name': 'Updated Game', 'uuid': str(self.game.uuid), 'genre': 'RPG'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Game.objects.get(uuid=self.game.uuid).name, data['name'])

    def test_delete_game(self):
        url = reverse('game-detail', args=[str(self.game.uuid)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Game.objects.count(), 0)

    def test_list_games(self):
        url = reverse('game-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
