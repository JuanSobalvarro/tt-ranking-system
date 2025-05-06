import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class CoreAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token_url = reverse('core:api_token')
        self.token_refresh_url = reverse('core:api_token_refresh')
        self.home_url = reverse('core:home')

    def test_obtain_token(self):
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        # Obtain token first
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword'})
        refresh_token = response.data['refresh']

        # Refresh token
        response = self.client.post(self.token_refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_home_view(self):
        # Obtain token first
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword'})
        access_token = response.data['access']

        # Access home view with token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('matchesPlayed', response.data)
