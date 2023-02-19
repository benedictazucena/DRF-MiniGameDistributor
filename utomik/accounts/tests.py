from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):

    def test_create_user(self):
        url = reverse('users-list')
        data = {
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'birthday': '2000-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@test.com')

    def test_create_user_invalid_email(self):
        url = reverse('users-list')
        data = {
            'email': 'testuser',  # invalid email address
            'password': 'testpassword',
            'birthday': '2000-01-01'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_under_18(self):
        url = reverse('users-list')
        data = {
            'email': 'testuser@test.com',
            'password': 'testpassword',
            'birthday': '2020-01-01'  # user is under 18
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_users(self):
        User.objects.create(email='testuser1@test.com', password='testpassword', birthday='2000-01-01')
        User.objects.create(email='testuser2@test.com', password='testpassword', birthday='2000-01-01')
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
