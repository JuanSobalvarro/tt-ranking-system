from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import UserProfileViewSet, PlayerProfileViewSet, RefereeProfileViewSet

app_name = 'profiles'

router = DefaultRouter()
router.register(r'base-users', UserProfileViewSet)
router.register(r'players', PlayerProfileViewSet)
router.register(r'referees', RefereeProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]