from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import UserProfile, PlayerProfile, RefereeProfile

@receiver(post_save, sender=PlayerProfile)
def update_is_player_flag(sender, instance: PlayerProfile, **kwargs):
    profile = instance.profile
    if not profile.is_player:
        profile.is_player = True
        profile.save(update_fields=['is_player'])

@receiver(post_save, sender=RefereeProfile)
def update_is_referee_flag(sender, instance: RefereeProfile, **kwargs):
    profile = instance.profile
    if not profile.is_referee:
        profile.is_referee = True
        profile.save(update_fields=['is_referee'])

