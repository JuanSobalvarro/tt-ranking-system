from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from profiles.models import UserProfile, PlayerProfile, RefereeProfile
from seasons.models import Season
from rankings.models import Ranking
from .models import SinglesMatch, SinglesGame, DoublesMatch, DoublesGame


class SinglesMatchTest(TestCase):
    def setUp(self):
        # Create players and season
        self.user1 = User
        self.player1 = PlayerProfile.objects.create(first_name="Player 1")
        self.player2 = PlayerProfile.objects.create(name="Player 2")
        self.season = Season.objects.create(name="2025 Season", start_date="2025-01-01", end_date="2025-12-31")

    def test_cannot_create_singles_match_same_player(self):
        match = SinglesMatch(player1=self.player1, player2=self.player1, date=datetime.now())
        with self.assertRaises(ValidationError):
            match.full_clean()

    def test_update_winner_logic(self):
        match = SinglesMatch.objects.create(player1=self.player1, player2=self.player2, season=self.season)
        # Create games with player1 winning two games
        SinglesGame.objects.create(match=match, player1_score=11, player2_score=5)
        SinglesGame.objects.create(match=match, player1_score=11, player2_score=9)
        SinglesGame.objects.create(match=match, player1_score=5, player2_score=11)

        match.update_winner()
        self.assertEqual(match.winner, self.player1)

    def test_save_triggers_winner_update(self):
        match = SinglesMatch.objects.create(player1=self.player1, player2=self.player2, season=self.season)
        SinglesGame.objects.create(match=match, player1_score=11, player2_score=5)
        match.save()  # triggers update_winner

        self.assertEqual(match.winner, self.player1)

    def test_signals_update_rankings(self):
        # Rankings start empty
        Ranking.objects.all().delete()

        match = SinglesMatch.objects.create(player1=self.player1, player2=self.player2, season=self.season)
        SinglesGame.objects.create(match=match, player1_score=11, player2_score=5)
        match.save()  # triggers signal

        r1 = Ranking.objects.get(player=self.player1, season=self.season)
        r2 = Ranking.objects.get(player=self.player2, season=self.season)

        # After match, player1 ranking should reflect a win, player2 a loss
        self.assertTrue(r1.wins > 0 or r1.matches > 0)
        self.assertTrue(r2.matches > 0)

    def test_singles_game_scores_equal_raises(self):
        match = SinglesMatch.objects.create(player1=self.player1, player2=self.player2, season=self.season)
        game = SinglesGame(match=match, player1_score=10, player2_score=10)
        with self.assertRaises(ValidationError):
            game.full_clean()


class DoublesMatchTest(TestCase):
    def setUp(self):
        self.p1 = PlayerProfile.objects.create(name="P1")
        self.p2 = PlayerProfile.objects.create(name="P2")
        self.p3 = PlayerProfile.objects.create(name="P3")
        self.p4 = PlayerProfile.objects.create(name="P4")
        self.season = Season.objects.create(name="2025 Season", start_date="2025-01-01", end_date="2025-12-31")

    def test_clean_validates_unique_players(self):
        with self.assertRaises(ValidationError):
            DoublesMatch(
                team1_player1=self.p1, team1_player2=self.p1,
                team2_player1=self.p3, team2_player2=self.p4,
                date=datetime.now(), season=self.season
            ).full_clean()

        with self.assertRaises(ValidationError):
            DoublesMatch(
                team1_player1=self.p1, team1_player2=self.p2,
                team2_player1=self.p2, team2_player2=self.p4,
                date=datetime.now(), season=self.season
            ).full_clean()

    def test_update_winner_logic(self):
        match = DoublesMatch.objects.create(
            team1_player1=self.p1, team1_player2=self.p2,
            team2_player1=self.p3, team2_player2=self.p4,
            date=datetime.now(), season=self.season
        )
        # Simulate games where team 1 wins 2 games
        from .models import DoublesGame
        DoublesGame.objects.create(match=match, team1_score=11, team2_score=8)
        DoublesGame.objects.create(match=match, team1_score=11, team2_score=9)
        DoublesGame.objects.create(match=match, team1_score=8, team2_score=11)

        match.update_winner()
        self.assertEqual(match.winner_1, self.p1)
        self.assertEqual(match.winner_2, self.p2)

    # You can add similar signal and save tests for doubles matches here...

