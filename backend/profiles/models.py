from django.contrib.auth.models import User
from django.db import models
from players.models import Player


class PlayerProfile(User):
    """
    PlayerProfile model that extends the User model. When a player is created a player profile should be created.
    """
    class Meta:
        verbose_name = "PlayerProfile"
        verbose_name_plural = "PlayersProfiles"

    player = models.OneToOneField(Player, on_delete=models.CASCADE)


class RefereeProfile(User):
    """
    RefereeProfile model that extends the User model. When a referee is created a referee profile should be created.
    """
    class Meta:
        verbose_name = "RefereeProfile"
        verbose_name_plural = "RefereesProfiles"
