# ttranking/seasons/tests.py
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from seasons.models import Season
from django.contrib.auth.models import User

class SeasonModelTests(TestCase):
    def setUp(self):
        self.season = Season.objects.create(
            name='Test Season',
            start_date='2020-01-01',
            end_date='2020-12-31'
        )

    def test_get_season_for_datetime(self):
        dt = datetime.strptime("2020-07-15", "%Y-%m-%d")
        season = Season.get_season_for_datetime(dt)
        self.assertEqual(season, self.season)

    def test_get_season_for_datetime_no_match(self):
        dt = datetime.strptime("2021-01-01", "%Y-%m-%d")
        season = Season.get_season_for_datetime(dt)
        self.assertIsNone(season)

class SeasonAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.season = Season.objects.create(
            name="Summer 2024",
            start_date="2024-06-01",
            end_date="2024-08-31"
        )
        self.season_url = reverse('seasons:season-detail', args=[self.season.id])

        # Create users
        self.admin_user = User.objects.create_superuser('admin', '', 'admin')
        self.user = User.objects.create_user('user', '', 'user')

        # Get tokens for authentication
        self.token_admin = self.get_token('admin', 'admin')
        self.token_user = self.get_token('user', 'user')

    def get_token(self, username, password):
        url = reverse('core:api_token')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_list_seasons(self):
        url = reverse('seasons:season-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_season(self):
        url = reverse('seasons:season-list')
        data = {
            "name": "Winter 2024",
            "start_date": "2024-12-01",
            "end_date": "2025-02-28"
        }

        # Unauthenticated test
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated as user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated as admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_season(self):
        response = self.client.get(self.season_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_season(self):
        data = {"name": "Updated Summer 2024"}

        # Unauthenticated test
        response = self.client.patch(self.season_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated as user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.patch(self.season_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated as admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.patch(self.season_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.season.refresh_from_db()
        self.assertEqual(self.season.name, "Updated Summer 2024")

    def test_delete_season(self):
        # Unauthenticated test
        response = self.client.delete(self.season_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated as user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.delete(self.season_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated as admin
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(self.season_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Season.objects.filter(id=self.season.id).exists())