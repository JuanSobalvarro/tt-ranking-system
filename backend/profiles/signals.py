# backend/profiles/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from players.models import Player
from .models import PlayerProfile
from django.utils.crypto import get_random_string

@receiver(post_save, sender=Player)
def create_player_profile(sender, instance: Player, created, **kwargs):
    if created:
        username = instance.first_name + "_" + instance.last_name
        # Generate random password
        password = get_random_string(length=8)
        PlayerProfile.objects.create(username=username, player=instance, password=password)