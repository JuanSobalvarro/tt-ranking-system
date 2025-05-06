from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from collections import defaultdict

from players.models import Player, Ranking
from seasons.models import Season

from .models import SinglesMatch, DoublesMatch, SinglesGame, DoublesGame
from .serializers import SinglesMatchSerializer, DoublesMatchSerializer, SinglesGameSerializer, DoublesGameSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny


@api_view(['GET'])
def match_count_integrity(request):
    """
    Populates match count for every player in all seasons.
    """
    season_id = request.query_params.get('season')
    if not season_id:
        return Response({'error': 'Season parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return Response({'error': 'Season not found'}, status=status.HTTP_404_NOT_FOUND)

    response = {}

    # Get all rankings for the given season
    players_ranking = Ranking.objects.filter(season=season).select_related("player")

    # Create a hashmap for match counts and win counts
    single_match_counts = defaultdict(int)
    double_match_counts = defaultdict(int)
    singles_wins = defaultdict(int)
    doubles_wins = defaultdict(int)

    # Fetch all matches once and populate hashmaps
    singles_matches = SinglesMatch.objects.filter(season=season).only("player1", "player2", "winner")
    doubles_matches = DoublesMatch.objects.filter(season=season).only("team1_player1", "team1_player2", "team2_player1",
                                                                      "team2_player2", "winner_1", "winner_2")

    for match in singles_matches:
        single_match_counts[match.player1_id] += 1
        single_match_counts[match.player2_id] += 1
        if match.winner_id:
            singles_wins[match.winner_id] += 1

    for match in doubles_matches:
        for player_id in [match.team1_player1_id, match.team1_player2_id, match.team2_player1_id,
                          match.team2_player2_id]:
            double_match_counts[player_id] += 1
        if match.winner_1_id:
            doubles_wins[match.winner_1_id] += 1
        if match.winner_2_id:
            doubles_wins[match.winner_2_id] += 1

    # Track rankings that need to be updated
    rankings_to_update = []

    for player_ranking in players_ranking:
        player_id = player_ranking.player_id
        season = player_ranking.season
        new_single_match_count = single_match_counts.get(player_id, 0)
        new_double_match_count = double_match_counts.get(player_id, 0)
        new_match_count = new_single_match_count + new_double_match_count
        new_singles_wins = singles_wins.get(player_id, 0)
        new_doubles_wins = doubles_wins.get(player_id, 0)

        singles_losses = new_single_match_count - new_singles_wins
        doubles_losses = new_double_match_count - new_doubles_wins
        new_ranking = new_singles_wins * season.singles_points_for_win - singles_losses * season.singles_points_for_loss + \
                        new_doubles_wins * season.doubles_points_for_win - doubles_losses * season.doubles_points_for_loss

        updates = []
        if player_ranking.matches_played != new_match_count:
            updates.append(f"Match count updated from {player_ranking.matches_played} to {new_match_count}")
            player_ranking.singles_matches_played = new_single_match_count
            player_ranking.doubles_matches_played = new_double_match_count

        if player_ranking.singles_victories != new_singles_wins:
            updates.append(f"Singles wins updated from {player_ranking.singles_victories} to {new_singles_wins}")
            player_ranking.singles_victories = new_singles_wins

        if player_ranking.doubles_victories != new_doubles_wins:
            updates.append(f"Doubles wins updated from {player_ranking.doubles_victories} to {new_doubles_wins}")
            player_ranking.doubles_victories = new_doubles_wins

        if player_ranking.ranking != new_ranking:
            updates.append(f"Ranking updated from {player_ranking.ranking} to {new_ranking}")
            player_ranking.ranking = new_ranking


        if updates:
            rankings_to_update.append(player_ranking)
            response[player_ranking.id] = f"Player {player_ranking.player.full_name}: " + "; ".join(updates)
        else:
            response[player_ranking.id] = f"Match count for player {player_ranking.player.full_name} is correct"

    # Bulk update rankings
    if rankings_to_update:
        Ranking.objects.bulk_update(rankings_to_update, ["ranking", "singles_matches_played", "doubles_matches_played", "singles_victories", "doubles_victories"])

    return Response(response, status=status.HTTP_200_OK)


class GamePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SinglesGameViewSet(viewsets.ModelViewSet):
    queryset = SinglesGame.objects.all()
    serializer_class = SinglesGameSerializer
    pagination_class = GamePagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = SinglesGame.objects.all()
        match = self.request.query_params.get('match_id', None)
        if match is not None:
            queryset = queryset.filter(match=match)
        return queryset


class DoublesGameViewSet(viewsets.ModelViewSet):
    queryset = DoublesGame.objects.all()
    serializer_class = DoublesGameSerializer
    pagination_class = GamePagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class MatchPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class SinglesMatchViewSet(viewsets.ModelViewSet):
    queryset = SinglesMatch.objects.all().order_by('-date')
    serializer_class = SinglesMatchSerializer
    pagination_class = MatchPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = SinglesMatch.objects.all()
        season = self.request.query_params.get('season_id', None)
        if season is not None:
            queryset = queryset.filter(season=season)
        return queryset.order_by('-date')


class DoublesMatchViewSet(viewsets.ModelViewSet):
    queryset = DoublesMatch.objects.all().order_by('-date')
    serializer_class = DoublesMatchSerializer
    pagination_class = MatchPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = DoublesMatch.objects.all()
        season = self.request.query_params.get('season_id', None)
        if season is not None:
            queryset = queryset.filter(season=season)
        return queryset.order_by('-date')