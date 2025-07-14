from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Player

class PlayerAPITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', '', 'admin')
        self.user = User.objects.create_user('user', '', 'user')
        self.player1 = Player.objects.create(
            first_name="John",
            last_name="Doe",
            alias="JD",
            gender="M",
            date_of_birth="1990-01-01",
            nationality="US",
        )
        self.player2 = Player.objects.create(
            first_name="Jane",
            last_name="Smith",
            alias="JS",
            gender="F",
            date_of_birth="1992-02-02",
            nationality="GB",
        )

        self.token_admin = self.get_token('admin', 'admin')
        self.token_user = self.get_token('user', 'user')

    def get_token(self, name, password):
        url = reverse('core:api_token')
        data = {
            'username': name,
            'password': password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_country_choices(self):
        url = reverse('players:country-choices')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)

    def test_create_unauthenticated(self):
        url = reverse('players:player-list')
        data = {
            'first_name': 'Alice',
            'last_name': 'Wonderland',
            'alias': 'AW',
            'gender': 'F',
            'date_of_birth': '1995-05-05',
            'nationality': 'US',
            'ranking': 300,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated(self):
        url = reverse('players:player-list')
        data = {
            'first_name': 'Alice',
            'last_name': 'Wonderland',
            'alias': 'AW',
            'gender': 'F',
            'date_of_birth': '1995-05-05',
            'nationality': 'US',
            'ranking': 300,
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_admin(self):
        url = reverse('players:player-list')
        data = {
            'first_name': 'Alice',
            'last_name': 'Wonderland',
            'alias': 'AW',
            'gender': 'F',
            'date_of_birth': '1995-05-05',
            'nationality': 'US',
            'ranking': 300,
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_unauthenticated(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_retrieve_authenticated(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_retrieve_admin(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')


    def test_update_unauthenticated(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        data = {'ranking': 150}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_authenticated(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        data = {'ranking': 150}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_admin(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        data = {'ranking': 150}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ranking'], 150)

    def test_delete_unauthenticated(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_authenticated(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_admin(self):
        url = reverse('players:player-detail', args=[self.player1.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
