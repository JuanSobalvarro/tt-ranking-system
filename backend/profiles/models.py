from django.contrib.auth.models import User
from django.db import models
from players.models import Player


class PlayerProfile(User):
    """
    PlayerProfile model that extends the User model. When a player is created a player profile should be created.
    """

    player = models.OneToOneField(Player, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "PlayerProfile"
        verbose_name_plural = "PlayersProfiles"
