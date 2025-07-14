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