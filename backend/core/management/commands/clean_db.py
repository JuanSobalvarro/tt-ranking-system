from django.core.management.base import BaseCommand
from players.models import Player, Ranking


class Command(BaseCommand):
    help = 'Clean the database before doing a flush'

    def handle(self, *args, **kwargs):
        # Delete dependent data first
        Ranking.objects.all().delete()
        Player.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Database cleaned successfully.'))
