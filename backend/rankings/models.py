from django.db import models
from typing import Tuple
from seasons.models import Season
from profiles.models import PlayerProfile
from core.models import SoftDeleteModel


class Ranking(SoftDeleteModel):
    player_profile = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='rankings')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='player_rankings')

    # statistics
    ranking = models.IntegerField(default=0)
    singles_matches_played = models.IntegerField(default=0)
    doubles_matches_played = models.IntegerField(default=0)
    doubles_victories = models.IntegerField(default=0)
    singles_victories = models.IntegerField(default=0)

    class Meta:
        unique_together = ('player_profile', 'season')

    @property
    def matches_played(self):
        return self.singles_matches_played + self.doubles_matches_played

    @property
    def victories(self):
        return self.doubles_victories + self.singles_victories

    @property
    def winrate(self):
        if self.matches_played == 0:
            return 0
        return round((self.victories / self.matches_played) * 100, 2)

    def get_season_points(self, match_type: str) -> Tuple[int, int]:
        """
        Get the points for a win and a loss correspoding to the season assigned for the given match type
        (singles or doubles)
        :param match_type:
        :return:
        """
        if match_type not in ['singles', 'doubles']:
            raise ValueError("Invalid match type, must be 'singles' or 'doubles'")

        season = self.season
        if match_type == 'singles':
            return season.singles_points_for_win, season.singles_points_for_loss
        elif match_type == 'doubles':
            return season.doubles_points_for_win, season.doubles_points_for_loss

        return 0, 0

    @staticmethod
    def populate_ranking(player_profile: PlayerProfile):
        """
        This functions ensures that a player has a ranking model in the system for every season
        :param player_profile:
        :return:
        """
        seasons = Season.objects.all()

        # Validate if there is no season
        if not seasons.exists():
            raise ValueError("There are no seasons in the system")

        for season in seasons:
            if not Ranking.objects.filter(player_profile=player_profile, season=season).exists():
                Ranking.objects.create(player_profile=player_profile, season=season)
                print(f"Created ranking for {player_profile} in {season}")

    def _add_points(self, points):
        self.ranking += points
        self.save()

    def _remove_points(self, points):
        self.ranking -= points
        self.save()

    def _add_victory(self, match_type: str):
        """
        Add a victory to the player's ranking, the two types are 'singles' and 'doubles'
        :param match_type:
        :return:
        """
        # Validate the victory type
        if match_type not in ['singles', 'doubles']:
            raise ValueError("Invalid victory type, must be 'singles' or 'doubles'")

        if match_type == 'singles':
            self.singles_victories += 1
        elif match_type == 'doubles':
            self.doubles_victories += 1

        # Add points to ranking
        win_points, lose_points = self.get_season_points(match_type)
        self._add_points(win_points)

        self.save()

    def _remove_victory(self, match_type: str):
        """
        Remove a victory from the player's ranking, the two types are 'singles' and 'doubles'
        :param match_type:
        :return:
        """
        # Validate the victory type
        if match_type not in ['singles', 'doubles']:
            raise ValueError("Invalid victory type, must be 'singles' or 'doubles")

        if match_type == 'singles':
            self.singles_victories -= 1
        elif match_type == 'doubles':
            self.doubles_victories -= 1

        # Remove points from ranking
        win_points, lose_points = self.get_season_points(match_type)
        self._remove_points(win_points)

        self.save()

    def _add_lose(self, match_type: str):
        """
        Add a loss to the player's ranking, the two types are 'singles' and 'doubles'
        :param match_type:
        :return:
        """
        # Validate the victory type
        if match_type not in ['singles', 'doubles']:
            raise ValueError("Invalid match type, must be 'singles' or 'doubles'")

        win_points, lose_points = self.get_season_points(match_type)
        self._remove_points(lose_points)

    def _remove_lose(self, match_type: str):
        """
        Remove a loss from the player's ranking, the two types are 'singles' and 'doubles'
        :param match_type:
        :return:
        """
        # Validate the victory type
        if match_type not in ['singles', 'doubles']:
            raise ValueError("Invalid match type, must be 'singles' or 'doubles'")

        win_points, lose_points = self.get_season_points(match_type)
        self._add_points(lose_points)

    def add_match(self, match_type: str, victory: bool):
        """
        Add a match to the player's ranking, the two types are 'singles' and 'doubles'
        :param match_type: The type of match, 'singles' or 'doubles'
        :param victory: A boolean indicating if the player won the match
        :return:
        """
        # Validate the victory type
        if match_type not in ['singles', 'doubles']:
            raise ValueError("Invalid match type, must be 'singles' or 'doubles'")

        if match_type == 'singles':
            self.singles_matches_played += 1
        elif match_type == 'doubles':
            self.doubles_matches_played += 1

        if victory:
            self._add_victory(match_type)
        else:
            self._add_lose(match_type)

        self.save()

    def remove_match(self, match_type: str, victory: bool):
        """
        Remove a match from the player's ranking, the two types are 'singles' and 'doubles'
        :param match_type: The type of match, 'singles' or 'doubles'
        :param victory: A boolean indicating if the player won the match
        :return:
        """
        # Validate the victory type
        if match_type not in ['singles', 'doubles']:
            raise ValueError("Invalid match type, must be 'singles' or 'doubles'")

        if match_type == 'singles':
            self.singles_matches_played -= 1
        elif match_type == 'doubles':
            self.doubles_matches_played -= 1

        if victory:
            self._remove_victory(match_type)
        else:
            self._remove_lose(match_type)

        self.save()

    @staticmethod
    def exists_or_create(player_profile: PlayerProfile, season: Season) -> 'Ranking':
        """
        Check if a ranking exists for a player, if not it will create a new one
        :param player_profile:
        :param season:
        :return Ranking:
        """

        if not Ranking.objects.filter(player_profile=player_profile, season=season).exists():
            return Ranking.objects.create(player_profile=player_profile, season=season)
        return Ranking.objects.get(player_profile=player_profile, season=season)

    def __str__(self):
        return f"{self.player} - {self.season.name}"
