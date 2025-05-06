# ttranking/core/views.py
from datetime import timezone

from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render
from django.db import models
from django.template import loader

from django.utils import timezone

from players.models import Player, Ranking
from players.serializers import PlayerSerializer, RankingSerializer

from matches.models import SinglesMatch, DoublesMatch
from matches.serializers import SinglesMatchSerializer, DoublesMatchSerializer

from seasons.models import Season
from seasons.serializers import SeasonSerializer


from django.urls import reverse

from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication



class APIRootView(APIView):
    """
    API root view
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response({
            'players': reverse('players:player-list'),
            'singles_matches': reverse('matches:singlesmatch-list'),
            'doubles_matches': reverse('matches:doublesmatch-list'),
            'seasons': reverse('seasons:season-list'),
        })

class HomeView(APIView):
    permission_classes = [AllowAny]

    def order_by_winrate(self, queryset):
        return sorted(queryset, key=lambda x: x.winrate, reverse=True)

    def get(self, request):
        current_season = Season.get_season_for_datetime(timezone.make_aware(timezone.datetime.now()))

        if not current_season:
            return Response({
                'matchesPlayed': 0,
                'currentSeason': None,
                'topPlayers': [],
                'topByWinrate': [],
                'ranking': [],
            })

        print(Ranking.objects.all())

        ranking = Ranking.objects.filter(season=current_season).order_by('-ranking')

        top = ranking[:3]

        top_winrate = self.order_by_winrate(ranking)[:6]

        matches_played = 0
        for _ in SinglesMatch.objects.filter(season=current_season):
            matches_played += 1

        for _ in DoublesMatch.objects.filter(season=current_season):
            matches_played += 1

        data = {
            'matchesPlayed': matches_played,
            'currentSeason': SeasonSerializer(current_season).data,
            'topPlayers': RankingSerializer(top, many=True).data,
            'topByWinrate': RankingSerializer(top_winrate, many=True).data,
            'ranking': RankingSerializer(ranking[:20], many=True).data,
        }

        return Response(data)

class AdminHomeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Number of registered players
        registered_players = Player.objects.all().count()

        # Timeframe calculations
        now = timezone.make_aware(timezone.datetime.now())
        three_days_ago = now - timezone.timedelta(days=3)
        one_week_ago = now - timezone.timedelta(days=7)

        # Single matches played in the last 3 days
        single_matches_played_last_3days = SinglesMatch.objects.filter(date__gte=three_days_ago).count()

        # Double matches played in the last 3 days
        double_matches_played_last_3days = DoublesMatch.objects.filter(date__gte=three_days_ago).count()

        # Most active players in the last week
        singles_matches_last_week = (
            SinglesMatch.objects.filter(date__gte=one_week_ago)
            .values('player1', 'player2')
            .annotate(matches_played=models.Count('id'))
        )
        doubles_matches_last_week = (
            DoublesMatch.objects.filter(date__gte=one_week_ago)
            .values('team1_player1', 'team1_player2', 'team2_player1', 'team2_player2')
            .annotate(matches_played=models.Count('id'))
        )

        # Aggregate matches for each player
        player_match_counts = {}
        for entry in singles_matches_last_week:
            for player in ['player1', 'player2']:
                player_match_counts[entry[player]] = player_match_counts.get(entry[player], 0) + entry['matches_played']

        for entry in doubles_matches_last_week:
            for player in ['team1_player1', 'team1_player2', 'team2_player1', 'team2_player2']:
                player_match_counts[entry[player]] = player_match_counts.get(entry[player], 0) + entry['matches_played']

        most_active_players_last_week = sorted(player_match_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        # Prepare response data
        data = {
            "registered_players": registered_players,
            "single_matches_played_last_3days": single_matches_played_last_3days,
            "double_matches_played_last_3days": double_matches_played_last_3days,
            "most_active_players_last_week": [
                {
                    "player_name": Player.objects.get(id=player_id).full_name,
                    "matches_played_last_week": matches_played,
                }
                for player_id, matches_played in most_active_players_last_week
            ],
        }

        return Response(data)
