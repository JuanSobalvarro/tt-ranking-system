# ttranking/players/management/commands/check_players_points.py
from django.core.management.base import BaseCommand
from players.models import Player
from matches.models import SinglesMatch, DoublesMatch

class Command(BaseCommand):
    help = 'Check and correct player points consistency'

    def handle(self, *args, **kwargs):
        # Retrieve all players
        players = Player.objects.all()

        for player in players:
            # Calculate expected points
            expected_points = self.calculate_expected_points(player)

            if player.ranking != expected_points:
                self.stdout.write(f'Updating points for player: {player}')
                player.ranking = expected_points
                player.save()

        self.stdout.write('Consistency check completed.')

    def calculate_expected_points(self, player):
        # This function calculates the expected points for a player
        # based on match results or any other logic
        points = 0

        # Calculate points from SinglesMatch
        for match in SinglesMatch.objects.filter(player1=player) | SinglesMatch.objects.filter(player2=player):
            if match.winner == player:
                points += 1  # or use WINNING_POINTS constant

        # Calculate points from DoublesMatch
        for match in DoublesMatch.objects.filter(team1_player1=player) | DoublesMatch.objects.filter(team1_player2=player) | \
                    DoublesMatch.objects.filter(team2_player1=player) | DoublesMatch.objects.filter(team2_player2=player):
            if match.winner_team == 'Team 1' and (match.team1_player1 == player or match.team1_player2 == player):
                points += 1  # or use WINNING_POINTS constant
            elif match.winner_team == 'Team 2' and (match.team2_player1 == player or match.team2_player2 == player):
                points += 1  # or use WINNING_POINTS constant

        return points
