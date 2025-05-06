# ttranking/matches/tests.py
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from matches.models import SinglesMatch, DoublesMatch, SinglesGame, DoublesGame
from players.models import Player
from seasons.models import Season


class MatchAPITests(APITestCase):
    def setUp(self):
        # Create users and players
        self.admin_user = User.objects.create_superuser('admin', '', 'admin')
        self.user = User.objects.create_user('user', '', 'user')
        # Create players with the correct fields
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
        self.player3 = Player.objects.create(
            first_name="Michael",
            last_name="Johnson",
            alias="MJ",
            gender="M",
            date_of_birth="1988-03-03",
            nationality="CA",
        )
        self.player4 = Player.objects.create(
            first_name="Emily",
            last_name="Davis",
            alias="ED",
            gender="F",
            date_of_birth="1995-04-04",
            nationality="AU",
        )

        self.season = Season.objects.create(
            name="2024 Season",
            description="Test",
            start_date="2024-01-01",
            end_date="2024-12-31",
            singles_points_for_win=4,
            singles_points_for_loss=2,
            doubles_points_for_win=2,
            doubles_points_for_loss=1,
        )

        # Get tokens for authentication
        self.token_admin = self.get_token('admin', 'admin')
        self.token_user = self.get_token('user', 'user')

    def get_token(self, username, password):
        url = reverse('core:api_token')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_create_singles_match(self):
        url = reverse('matches:singlesmatch-list')
        data = {
            'date': timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            'season': self.season.id,
            'player1': self.player1.id,
            'player2': self.player2.id,
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_doubles_match(self):
        url = reverse('matches:doublesmatch-list')
        data = {
            'date': timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            'season': self.season.id,
            'team1_player1': self.player1.id,
            'team1_player2': self.player2.id,
            'team2_player1': self.player3.id,
            'team2_player2': self.player4.id,
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_singles_game(self):
        match = SinglesMatch.objects.create(
            date=timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            season=self.season,
            player1=self.player1,
            player2=self.player2,
        )
        url = reverse('matches:singlesgame-list')
        data = {
            'match': match.id,
            'player1_score': 11,
            'player2_score': 9,
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_doubles_game(self):
        match = DoublesMatch.objects.create(
            date=timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            season=self.season,
            team1_player1=self.player1,
            team1_player2=self.player2,
            team2_player1=self.player3,
            team2_player2=self.player4,
        )
        url = reverse('matches:doublesgame-list')
        data = {
            'match': match.id,
            'team1_score': 11,
            'team2_score': 9,
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_singles_matches(self):
        url = reverse('matches:singlesmatch-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_doubles_matches(self):
        url = reverse('matches:doublesmatch-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_winner_single_match(self):
        url_match = reverse('matches:singlesmatch-list')
        url_game = reverse('matches:singlesgame-list')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)

        data_match = {
            'date': timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            'season': self.season.id,
            'player1': self.player1.id,
            'player2': self.player2.id,
        }

        response_match = self.client.post(url_match, data_match, format='json')

        data_game1 = {
            'match': response_match.data["id"],
            'player1_score': 11,
            'player2_score': 9,
        }
        data_game2 = {
            'match': response_match.data["id"],
            'player1_score': 9,
            'player2_score': 11,
        }
        data_game3 = {
            'match': response_match.data["id"],
            'player1_score': 11,
            'player2_score': 9,
        }

        response_game1 = self.client.post(url_game, data_game1, format='json')
        response_game2 = self.client.post(url_game, data_game2, format='json')
        response_game3 = self.client.post(url_game, data_game3, format='json')

        self.assertEqual(response_match.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SinglesMatch.objects.get(pk=response_match.data["id"]).winner, self.player1)

    def test_winner_double_match(self):
        url_match = reverse('matches:doublesmatch-list')
        url_game = reverse('matches:doublesgame-list')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)

        data_match = {
            'date': timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            'season': self.season.id,
            'team1_player1': self.player1.id,
            'team1_player2': self.player2.id,
            'team2_player1': self.player3.id,
            'team2_player2': self.player4.id,
        }

        response_match = self.client.post(url_match, data_match, format='json')

        data_game1 = {
            'match': response_match.data["id"],
            'team1_score': 11,
            'team2_score': 9,
        }
        data_game2 = {
            'match': response_match.data["id"],
            'team1_score': 9,
            'team2_score': 11,
        }
        data_game3 = {
            'match': response_match.data["id"],
            'team1_score': 11,
            'team2_score': 9,
        }

        response_game1 = self.client.post(url_game, data_game1, format='json')
        response_game2 = self.client.post(url_game, data_game2, format='json')
        response_game3 = self.client.post(url_game, data_game3, format='json')

        self.assertEqual(response_match.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoublesMatch.objects.get(pk=response_match.data["id"]).winner_1, self.player1)
        self.assertEqual(DoublesMatch.objects.get(pk=response_match.data["id"]).winner_2, self.player2)

    def test_delete_singles_match(self):
        url = reverse('matches:singlesmatch-list')
        match_data = {
            'date': timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            'season': self.season.id,
            'player1': self.player1.id,
            'player2': self.player2.id,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response_match = self.client.post(url, match_data, format='json')

        game_data ={
            'match': response_match.data["id"],
            'player1_score': 11,
            'player2_score': 9,
        }

        # Prev delete
        response_game = self.client.post(reverse('matches:singlesgame-list'), game_data, format='json')
        self.assertEqual(response_match.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, Player.objects.get(pk=self.player1.id).ranking)
        self.assertEqual(-2, Player.objects.get(pk=self.player2.id).ranking)

        # After delete
        response = self.client.delete(reverse('matches:singlesmatch-detail', args=[response_match.data['id']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Player.objects.get(pk=self.player1.id).ranking)
        self.assertEqual(0, Player.objects.get(pk=self.player2.id).ranking)

    def test_delete_doubles_match(self):
        url = reverse('matches:doublesmatch-list')
        match_data = {
            'date': timezone.make_aware(datetime.strptime('2024-08-20T10:00:00Z', '%Y-%m-%dT%H:%M:%SZ')),
            'season': self.season.id,
            'team1_player1': self.player1.id,
            'team1_player2': self.player2.id,
            'team2_player1': self.player3.id,
            'team2_player2': self.player4.id,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response_match = self.client.post(url, match_data, format='json')

        game_data ={
            'match': response_match.data["id"],
            'team1_score': 11,
            'team2_score': 9,
        }

        # Prev delete
        response_game = self.client.post(reverse('matches:doublesgame-list'), game_data, format='json')
        self.assertEqual(response_match.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_game.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Player.objects.get(pk=self.player1.id).ranking)
        self.assertEqual(2, Player.objects.get(pk=self.player2.id).ranking)
        self.assertEqual(-1, Player.objects.get(pk=self.player3.id).ranking)
        self.assertEqual(-1, Player.objects.get(pk=self.player4.id).ranking)

        # After delete
        response = self.client.delete(reverse('matches:doublesmatch-detail', args=[response_match.data['id']]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Player.objects.get(pk=self.player1.id).ranking)
        self.assertEqual(0, Player.objects.get(pk=self.player2.id).ranking)
        self.assertEqual(0, Player.objects.get(pk=self.player3.id).ranking)
        self.assertEqual(0, Player.objects.get(pk=self.player4.id).ranking)