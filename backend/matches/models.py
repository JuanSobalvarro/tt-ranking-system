from django.db import models
from django.db.transaction import commit
from django.utils.timezone import datetime
from django.core.exceptions import ValidationError
from players.models import Player, Ranking
from seasons.models import Season


class SinglesGame(models.Model):
    """
    A singles game is a game between two players.
    Fields: match, player1_score, player2_score, winner
    """
    match = models.ForeignKey('SinglesMatch', related_name='games', on_delete=models.CASCADE)
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
        self.update_match()

    def clean(self):
        if self.player1_score == self.player2_score:
            raise ValidationError("Scores cannot be equal.")

    def __str__(self):
        return f"Game: {self.player1_score} - {self.player2_score}"

class DoublesGame(models.Model):
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

class SinglesMatch(models.Model):
    """
    A singles match is a match between two players.
    Fields: date, season, player1, player2, winner
    """
    date = models.DateTimeField(default=datetime.now, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='singles_matches', blank=True, null=True)
    player1 = models.ForeignKey(Player, related_name='singles_matches_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='singles_matches_as_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, related_name='singles_matches_won', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def games_won(self):
        player1_wins = SinglesGame.objects.filter(match=self.id, winner=1).count()
        player2_wins = SinglesGame.objects.filter(match=self.id, winner=2).count()
        return player1_wins, player2_wins

    @property
    def players(self):
        return self.player1, self.player2

    @property
    def get_season(self):
        return Season.get_season_for_datetime(self.date)

    def update_winner(self):
        player1_wins, player2_wins = self.games_won
        # print("Game wins found: ", player1_wins, player2_wins)
        if player1_wins > player2_wins:
            self.winner = self.player1
        elif player2_wins > player1_wins:
            self.winner = self.player2
        else:
            self.winner = None

        print("Match winner updated: ", self.winner)

    def update_rankings(self):
        players_ranking = [Ranking.objects.get_or_create(player=player, season=self.season)[0] for player in self.players]

        # Check if the match is already created and remove the points from the previous winner and add points to the loser
        if self.pk:
            previous_match = SinglesMatch.objects.select_related('player1', 'player2').get(pk=self.pk)

            prev_players_ranking = [Ranking.objects.get_or_create(player=player, season=self.season)[0] for player in previous_match.players]

            print("Previous players ranking: ", prev_players_ranking)

            self.remove_match_from_players(prev_players_ranking[0], prev_players_ranking[1])

        self.add_match_to_players(players_ranking[0], players_ranking[1])

    def add_match_to_players(self, player1_ranking: Ranking, player2_ranking: Ranking):
        """
        This function calls the add_match function from ranking to each player
        :param player1_ranking:
        :param player2_ranking:
        :return:
        """
        # print("Updating points given winner: ", self.winner)
        if self.winner == self.player1:
            player1_ranking.add_match('singles', True)
            player2_ranking.add_match('singles', False)

        elif self.winner == self.player2:
            player1_ranking.add_match('singles', False)
            player2_ranking.add_match('singles', True)

    def remove_match_from_players(self, player1_ranking: Ranking, player2_ranking: Ranking):
        """
        This function calls the remove_match function from ranking to each player
        :param player1_ranking:
        :param player2_ranking:
        :return:
        """
        if self.winner == self.player1:
            player1_ranking.remove_match('singles', True)
            player2_ranking.remove_match('singles', False)
        elif self.winner == self.player2:
            player1_ranking.remove_match('singles', False)
            player2_ranking.remove_match('singles', True)

        print("Removing match from players")

    def save(self, *args, **kwargs):
        self.clean()

        if not self.season:
            self.season = self.get_season

        self.update_winner()
        if self.winner:
            self.update_rankings()
        print("Saving match with winner: ", self.winner)
        super().save(*args, **kwargs)

    def clean(self):
        if self.player1 == self.player2:
            raise ValidationError("Player 1 and Player 2 cannot be the same.")

    def delete(self, *args, **kwargs):
        player1_ranking = Ranking.objects.get_or_create(player=self.player1.pk, season=self.season)[0]
        player2_ranking = Ranking.objects.get_or_create(player=self.player2.pk, season=self.season)[0]

        if player1_ranking and player2_ranking:
            self.remove_match_from_players(player1_ranking, player2_ranking)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.player1} vs {self.player2} - {self.date}"


class DoublesMatch(models.Model):
    """
    A doubles match is a match between two teams of two players each.
    Fields: date, season, team1_player1, team1_player2, team2_player1, team2_player2, winner_1, winner_2
    """
    date = models.DateTimeField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='doubles_matches', blank=True, null=True)
    team1_player1 = models.ForeignKey(Player, related_name='doubles_matches_team1_player1', on_delete=models.CASCADE)
    team1_player2 = models.ForeignKey(Player, related_name='doubles_matches_team1_player2', on_delete=models.CASCADE)
    team2_player1 = models.ForeignKey(Player, related_name='doubles_matches_team2_player1', on_delete=models.CASCADE)
    team2_player2 = models.ForeignKey(Player, related_name='doubles_matches_team2_player2', on_delete=models.CASCADE)
    winner_1 = models.ForeignKey(Player, related_name='doubles_matches_won1', on_delete=models.CASCADE, null=True, blank=True)
    winner_2 = models.ForeignKey(Player, related_name='doubles_matches_won2', on_delete=models.CASCADE, null=True, blank=True)

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

    def update_rankings(self):
        players_ranking = [Ranking.objects.get_or_create(player=player, season=self.season)[0] for player in self.players]

        # Check if the match is already created
        if self.pk:
            previous_match = DoublesMatch.objects.select_related('team1_player1', 'team1_player2', 'team2_player1', 'team2_player2').get(pk=self.pk)

            prev_players_ranking = [Ranking.objects.get_or_create(player=player, season=self.season)[0] for player in previous_match.players]

            self.remove_match_from_players(prev_players_ranking[0], prev_players_ranking[1], prev_players_ranking[2], prev_players_ranking[3])

        self.add_match_to_players(players_ranking[0], players_ranking[1], players_ranking[2], players_ranking[3])

    def add_match_to_players(self, player1_ranking, player2_ranking, player3_ranking, player4_ranking):

        # print("Updating points given winner: ", self.winner)
        if self.winner_1 == self.team1_player1 and self.winner_2 == self.team1_player2:
            player1_ranking.add_match('doubles', True)
            player2_ranking.add_match('doubles', True)
            player3_ranking.add_match('doubles', False)
            player4_ranking.add_match('doubles', False)

        elif self.winner_1 == self.team2_player1 and self.winner_2 == self.team2_player2:
            player1_ranking.add_match('doubles', False)
            player2_ranking.add_match('doubles', False)
            player3_ranking.add_match('doubles', True)
            player4_ranking.add_match('doubles', True)

        print("Adding match to players")

    def remove_match_from_players(self, player1_ranking, player2_ranking, player3_ranking, player4_ranking):
        if self.winner_1 == self.team1_player1 and self.winner_2 == self.team1_player2:
            player1_ranking.remove_match('doubles', True)
            player2_ranking.remove_match('doubles', True)
            player3_ranking.remove_match('doubles', False)
            player4_ranking.remove_match('doubles', False)

        elif self.winner_1 == self.team2_player1 and self.winner_2 == self.team2_player2:
            player1_ranking.remove_match('doubles', False)
            player2_ranking.remove_match('doubles', False)
            player3_ranking.remove_match('doubles', True)
            player4_ranking.remove_match('doubles', True)

        print("Removing match from players")

    def check_rankings(self):
        """
        This functions validates that all players have a ranking for the season.
        :return:
        """
        season = Season.objects.get(pk=self.season.pk)
        if not Ranking.objects.filter(player=self.team1_player1, season=season).exists():
            raise ValidationError("Player 1 of team 1 does not have a ranking for the season.")
        if not Ranking.objects.filter(player=self.team1_player2, season=season).exists():
            raise ValidationError("Player 2 of team 1 does not have a ranking for the season.")
        if not Ranking.objects.filter(player=self.team2_player1, season=season).exists():
            raise ValidationError("Player 1 of team 2 does not have a ranking for the season.")
        if not Ranking.objects.filter(player=self.team2_player2, season=season).exists():
            raise ValidationError("Player 2 of team 2 does not have a ranking for the season.")

    def save(self, *args, **kwargs):
        self.clean()

        if not self.season:
            self.season = self.get_season

        if not self.season:
            raise ValidationError("There is not a season defined")

        # self.check_rankings()

        self.update_winner()
        self.update_rankings()
        # print("Saving doubles match with winners: ", self.winner_1, self.winner_2)
        super().save(*args, **kwargs)

    def clean(self):
        if self.team1_player1 == self.team1_player2 or self.team2_player1 == self.team2_player2:
            raise ValidationError("Players in the same team cannot be the same.")
        all_players = {self.team1_player1, self.team1_player2, self.team2_player1, self.team2_player2}
        if len(all_players) < 4:
            raise ValidationError("Players cannot be repeated across teams.")

    def delete(self, *args, **kwargs):
        player1_ranking = Ranking.objects.get_or_create(player=self.team1_player1.pk, season=self.season)[0]
        player2_ranking = Ranking.objects.get_or_create(player=self.team1_player2.pk, season=self.season)[0]
        player3_ranking = Ranking.objects.get_or_create(player=self.team2_player1.pk, season=self.season)[0]
        player4_ranking = Ranking.objects.get_or_create(player=self.team2_player2.pk, season=self.season)[0]

        if player1_ranking and player2_ranking and player3_ranking and player4_ranking:
            self.remove_match_from_players(player1_ranking, player2_ranking, player3_ranking, player4_ranking)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Team 1: {self.team1_player1} & {self.team1_player2} vs Team 2: {self.team2_player1} & {self.team2_player2} - {self.date}"
