from django.db import models
from django.contrib.auth.models import User

from backend.players.models import Player
from backend.matches.models import SinglesMatch, DoublesMatch, SinglesGame, DoublesGame
from backend.seasons.models import Season

from backend.tournaments.enums import SexType, TournamentStage, TournamentStatus, TournamentType

class Tournament(models.Model):
    """
    Abstract class for tournaments. The ITTF defines the following types of tournaments:
    - Single: A tournament with a single player.
    - Double: A tournament with a pair of players.
    - Team: A tournament with a team of players.
    So the tournament structure of matches phases can be: groups(round-robin) and knockout(single-elimination).
    """

    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    season = models.ForeignKey(Season, related_name='tournaments', on_delete=models.CASCADE)
    sex_type = models.CharField(max_length=1, choices=SexType.choices)
    referees = models.ManyToManyField(User, related_name='tournaments')

    class Meta:
        abstract = True


class SinglesTournament(Tournament):
    """
    A singles tournament is a tournament in which opponents compete individually.
    """
    matches = models.ManyToManyField(SinglesMatch, related_name="tournaments")


class SinglesGroup(models.Model):
    """
    Round-Robin phase of a tournament.
    """
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=255)
    players = models.ManyToManyField(Player, related_name="groups")


class Pair(models.Model):
    """
    Pair of players in a tournament.
    """
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="pair_player1")
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="pair_player2")
    tournament = models.ForeignKey(DoubleTournament, on_delete=models.CASCADE, related_name="pairs")


class SinglesTournament(Tournament):
    """
    Tournament with a single player.
    """
    tournament_type = TournamentType.Single
    groups = models.ManyToManyField(SinglesGroup, related_name="tournaments")
    matches = models.ManyToManyField(SinglesMatch, related_name="tournaments")
    games = models.ManyToManyField(SinglesGame, related_name="tournaments")
