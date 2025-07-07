from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ranking, Player
from seasons.models import Season


@receiver(post_save, sender=Player)
def create_ranking_for_new_player(sender, instance: Player, created, **kwargs):
    """
    Signal to create a ranking when a player is created.
    """
    if created:
        for season in Season.objects.all():
            # Create a ranking for each season
            Ranking.objects.create(player=instance, season=season)

@receiver(post_save, sender=Season)
def create_ranking_for_new_season(sender, instance: Season, created, **kwargs):
    """
    Signal to create rankings for all players when a new season is created.
    """
    if created:
        for player in Player.objects.all():
            # Create a ranking for each player
            Ranking.objects.create(player=player, season=instance)