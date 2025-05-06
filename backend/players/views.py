# ttrankin/players/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Player, Ranking
from .enums import CountryChoices
from .serializers import PlayerSerializer, RankingSerializer

PLAYERS_PER_PAGE = 6

@api_view(['GET'])
def country_choices(request):
    countries = CountryChoices.choices
    return Response(countries)


@api_view(['GET'])
def ranking_integrity(request):
    """
    Populates ranking for every player in all seasons
    :param request:
    :return:
    """
    response = {}

    players = Player.objects.all()
    for player in players:
        player.create_rankings()
        response[player.id] = f"Ranking verified for player {player.full_name}"

    return Response(response, status=status.HTTP_200_OK)

class PlayerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('first_name', 'last_name')
    serializer_class = PlayerSerializer
    pagination_class = PlayerPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    # def list(self, request):
    #     pass
    #
    # def create(self, request):
    #     pass
    #
    # def retrieve(self, request, pk=None):
    #     pass
    #
    # def update(self, request, pk=None):
    #     pass
    #
    # def partial_update(self, request, pk=None):
    #     pass
    #
    # def destroy(self, request, pk=None):
    #     pass

class RankingPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.all().order_by('-ranking')
    serializer_class = RankingSerializer
    pagination_class = RankingPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Get ranking given a season
        :return:
        """
        season = self.request.query_params.get('season_id', None)
        player = self.request.query_params.get('player_id', None)

        ranking = Ranking.objects.all().order_by('-ranking')
        if season and player:
            ranking = Ranking.objects.filter(season=season, player=player).order_by('-ranking')
        elif season:
            ranking = Ranking.objects.filter(season=season).order_by('-ranking')
        elif player:
            ranking = Ranking.objects.filter(player=player).order_by('-ranking')


        print("Returning rankings: ", ranking)

        return ranking

    # def list(self, request):
    #     pass
    #
    # def create(self, request):
    #     pass
    #
    # def retrieve(self, request, pk=None):
    #     pass
    #
    # def update(self, request, pk=None):
    #     pass
    #
    # def partial_update(self, request, pk=None):
    #     pass
    #
    # def destroy(self, request, pk=None):
    #     pass
