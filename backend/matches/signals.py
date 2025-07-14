from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import SinglesMatch, DoublesMatch
from rankings.models import Ranking
from seasons.models import Season
from profiles.models import PlayerProfile
from typing import List


@receiver(post_save, sender=SinglesMatch)
def update_singles_match_rankings(sender, instance: SinglesMatch, created, **kwargs):
    if not instance.winner:
        return

    season: Season  = instance.season
    player1: PlayerProfile = instance.player1
    player2: PlayerProfile = instance.player2

    ranking1: Ranking = Ranking.objects.get_or_create(player=player1, season=season)[0]
    ranking2: Ranking = Ranking.objects.get_or_create(player=player2, season=season)[0]

    if not created:
        previous = SinglesMatch.objects.get(pk=instance.pk)
        if previous.winner:
            ranking1.remove_match('singles', previous.winner == previous.player1)
            ranking2.remove_match('singles', previous.winner == previous.player2)

    ranking1.add_match('singles', instance.winner == player1)
    ranking2.add_match('singles', instance.winner == player2)


@receiver(pre_delete, sender=SinglesMatch)
def remove_singles_match_rankings(sender, instance: SinglesMatch, **kwargs):
    if not instance.winner:
        return

    season = instance.season
    ranking1 = Ranking.objects.get_or_create(player=instance.player1, season=season)[0]
    ranking2 = Ranking.objects.get_or_create(player=instance.player2, season=season)[0]

    ranking1.remove_match('singles', instance.winner == instance.player1)
    ranking2.remove_match('singles', instance.winner == instance.player2)


@receiver(post_save, sender=DoublesMatch)
def update_doubles_match_rankings(sender, instance: DoublesMatch, created, **kwargs):
    if not instance.winner_1 or not instance.winner_2:
        return

    season = instance.season
    players = instance.players
    rankings = [Ranking.objects.get_or_create(player=p, season=season)[0] for p in players]

    if not created:
        previous = DoublesMatch.objects.get(pk=instance.pk)
        if previous.winner_1 and previous.winner_2:
            remove_doubles_ranking(previous, rankings)

    add_doubles_ranking(instance, rankings)

@receiver(pre_delete, sender=DoublesMatch)
def remove_doubles_match_rankings(sender, instance: DoublesMatch, **kwargs):
    if not instance.winner_1 or not instance.winner_2:
        return

    rankings = [Ranking.objects.get_or_create(player=p, season=instance.season)[0] for p in instance.players]
    remove_doubles_ranking(instance, rankings)


def add_doubles_ranking(match: DoublesMatch, rankings: List[Ranking]):
    if match.winner_1 == match.team1_player1 and match.winner_2 == match.team1_player2:
        rankings[0].add_match('doubles', True)
        rankings[1].add_match('doubles', True)
        rankings[2].add_match('doubles', False)
        rankings[3].add_match('doubles', False)
    elif match.winner_1 == match.team2_player1 and match.winner_2 == match.team2_player2:
        rankings[0].add_match('doubles', False)
        rankings[1].add_match('doubles', False)
        rankings[2].add_match('doubles', True)
        rankings[3].add_match('doubles', True)

def remove_doubles_ranking(match: DoublesMatch, rankings: List[Ranking]):
    if match.winner_1 == match.team1_player1 and match.winner_2 == match.team1_player2:
        rankings[0].remove_match('doubles', True)
        rankings[1].remove_match('doubles', True)
        rankings[2].remove_match('doubles', False)
        rankings[3].remove_match('doubles', False)
    elif match.winner_1 == match.team2_player1 and match.winner_2 == match.team2_player2:
        rankings[0].remove_match('doubles', False)
        rankings[1].remove_match('doubles', False)
        rankings[2].remove_match('doubles', True)
        rankings[3].remove_match('doubles', True)
