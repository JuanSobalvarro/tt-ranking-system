# ttranking/players/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, RankingViewSet, country_choices, ranking_integrity

app_name = 'players'

# Default routes for api consistency
router = DefaultRouter()
router.register(r'player', PlayerViewSet)
router.register(r'ranking', RankingViewSet)

# print(router.urls)

urlpatterns = [
    path('country-choices/', country_choices, name='country-choices'),
    path('ranking-integrity/', ranking_integrity, name='ranking-integrity'),
    path('', include(router.urls)),
]
