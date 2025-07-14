from django.db import models
from django.utils.timezone import datetime
from django.core.exceptions import ValidationError
from core.models import SoftDeleteModel
from profiles.models import PlayerProfile, RefereeProfile
from rankings.models import Ranking
from seasons.models import Season


class SinglesGame(SoftDeleteModel):
    """
    A singles game is a game between two players.
    Fields: match, player1_score, player2_score, winner
    """
    match = models.ForeignKey('SinglesMatch', related_name='singles_games', on_delete=models.CASCADE)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    winner = models.IntegerField(blank=True, null=True)

    def update_match(self):
        match = SinglesMatch.objects.get(pk=self.match.pk)
        match.save()

    def update_winner(self):
        if self.player1_score > self.player2_score:
            self.winner = 1
        elif self.player2_score > self.player1_score:
            self.winner = 2
        else:
            self.winner = None
        # print("Game winner updated: ", self.winner)

    def save(self, *args, **kwargs):
        self.clean()
        self.update_winner()
        super().save(*args, **kwargs)

    def clean(self):
        if self.player1_score == self.player2_score:
            raise ValidationError("Scores cannot be equal.")

    def __str__(self):
        return f"Game: {self.player1_score} - {self.player2_score}"

class DoublesGame(SoftDeleteModel):
    """
    A doubles game is a game between two teams of two players each.
    Fields: match, team1_score, team2_score, winner
    """
    match = models.ForeignKey('DoublesMatch', related_name='games', on_delete=models.CASCADE)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    winner = models.IntegerField(blank=True, null=True)

    def update_match(self):
        match = DoublesMatch.objects.get(pk=self.match.pk)
        match.save()

    def update_winner(self):
        if self.team1_score > self.team2_score:
            self.winner = 1
        elif self.team2_score > self.team1_score:
            self.winner = 2
        else:
            self.winner = None
        # print("Game winner updated: ", self.winner)

    def save(self, *args, **kwargs):
        self.clean()
        self.update_winner()
        super().save(*args, **kwargs)
        self.update_match()

    def clean(self):
        if self.team1_score == self.team2_score:
            raise ValidationError("Scores cannot be equal.")

    def __str__(self):
        return f"Game: {self.team1_score} - {self.team2_score}"

class SinglesMatch(SoftDeleteModel):
    """
    A singles match is a match between two players.
    Fields: date, season, player1, player2, winner
    """
    date = models.DateTimeField(default=datetime.now, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='singles_matches', blank=True, null=True)
    player1 = models.ForeignKey(PlayerProfile, related_name='singles_matches_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(PlayerProfile, related_name='singles_matches_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(PlayerProfile, related_name='singles_matches_won', on_delete=models.CASCADE, null=True, blank=True)
    referee = models.ForeignKey(RefereeProfile, related_name='singles_matches_referee', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def games_won(self):
        player1_wins = self.singles_games.filter(winner=1)
        player2_wins = self.singles_games.filter(winner=2)
        return player1_wins.count(), player2_wins.count()

    @property
    def player1_games(self):
        return self.singles_games.filter(winner=1)

    @property
    def player2_games(self):
        return self.singles_games.filter(winner=2)

    @property
    def games(self):
        return self.singles_games.all()

    @property
    def players(self):
        return self.player1, self.player2

    @property
    def get_season(self):
        return Season.get_season_for_datetime(self.date)

    def update_winner(self):
        player1_wins, player2_wins = self.games_won

        if player1_wins > player2_wins:
            self.winner = self.player1
        elif player2_wins > player1_wins:
            self.winner = self.player2
        else:
            self.winner = None

    def save(self, *args, **kwargs):
        self.clean()

        if not self.season:
            self.season = self.get_season

        self.update_winner()
        super().save(*args, **kwargs)

    def clean(self):
        if self.player1 == self.player2:
            raise ValidationError("Player 1 and Player 2 cannot be the same.")

    def __str__(self):
        return f"{self.player1} vs {self.player2} - {self.date}"


class DoublesMatch(SoftDeleteModel):
    """
    A doubles match is a match between two teams of two players each.
    Fields: date, season, team1_player1, team1_player2, team2_player1, team2_player2, winner_1, winner_2
    """
    date = models.DateTimeField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='doubles_matches', blank=True, null=True)
    team1_player1 = models.ForeignKey(PlayerProfile, related_name='doubles_matches_team1_player1', on_delete=models.CASCADE)
    team1_player2 = models.ForeignKey(PlayerProfile, related_name='doubles_matches_team1_player2', on_delete=models.CASCADE)
    team2_player1 = models.ForeignKey(PlayerProfile, related_name='doubles_matches_team2_player1', on_delete=models.CASCADE)
    team2_player2 = models.ForeignKey(PlayerProfile, related_name='doubles_matches_team2_player2', on_delete=models.CASCADE)
    winner_1 = models.ForeignKey(PlayerProfile, related_name='doubles_matches_won1', on_delete=models.CASCADE, null=True, blank=True)
    winner_2 = models.ForeignKey(PlayerProfile, related_name='doubles_matches_won2', on_delete=models.CASCADE, null=True, blank=True)
    referee = models.ForeignKey(RefereeProfile, related_name='doubles_matches_referee', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def winners(self):
        return self.winner_1, self.winner_2

    @property
    def get_season(self):
        return Season.get_season_for_datetime(self.date)

    @property
    def players(self):
        return self.team1_player1, self.team1_player2, self.team2_player1, self.team2_player2

    @property
    def games_won(self):
        """
        Returns the number of games won by each team.

        This is achieved by counting the number of games where the team1_score is greater than the team2_score and
        vice versa for the games that have a relation with the match.
        :return:
        """
        team1_wins = DoublesGame.objects.filter(match=self.id, winner=1).count()
        team2_wins = DoublesGame.objects.filter(match=self.id, winner=2).count()
        return team1_wins, team2_wins

    def update_winner(self):
        team1_wins, team2_wins = self.games_won
        if team1_wins > team2_wins:
            self.winner_1 = self.team1_player1
            self.winner_2 = self.team1_player2
        elif team2_wins > team1_wins:
            self.winner_1 = self.team2_player1
            self.winner_2 = self.team2_player2
        else:
            self.winner_1 = None
            self.winner_2 = None

    def save(self, *args, **kwargs):
        self.clean()
        if not self.season:
            self.season = self.get_season
        if not self.season:
            raise ValidationError("There is not a season defined for match's date.")

        self.update_winner()
        super().save(*args, **kwargs)

    def clean(self):
        if self.team1_player1 == self.team1_player2 or self.team2_player1 == self.team2_player2:
            raise ValidationError("Players in the same team cannot be the same.")
        all_players = {self.team1_player1, self.team1_player2, self.team2_player1, self.team2_player2}
        if len(all_players) < 4:
            raise ValidationError("Players cannot be repeated across teams.")

    def __str__(self):
        return f"Team 1: {self.team1_player1} & {self.team1_player2} vs Team 2: {self.team2_player1} & {self.team2_player2} - {self.date}"
