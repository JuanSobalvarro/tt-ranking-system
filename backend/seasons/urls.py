from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeasonViewSet, season_for_date

app_name = 'seasons'

router = DefaultRouter()
router.register(r'', SeasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('for-date/', season_for_date, name='season-for-date'),
]