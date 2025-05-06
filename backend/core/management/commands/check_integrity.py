# ttranking/core/management/commands/check_integrity.py
import os
from django.conf import settings
from django.core.management import BaseCommand
from players.models import Player
from matches.models import SinglesMatch, DoublesMatch, WINNING_POINTS, LOSING_POINTS


class Command(BaseCommand):
    help = 'Check integrity of players\' data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ranking',
            action='store_true',
            help='Check and update player rankings'
        )
        parser.add_argument(
            '--matchcount',
            action='store_true',
            help='Update match counts for each player'
        )
        parser.add_argument(
            '--cleanphotos',
            action='store_true',
            help='Delete all players photos not being used in media folder'
        )
        parser.add_argument(
            '--correctseason',
            action='store_true',
            help='Correct season for all matches'
        )

    def handle(self, *args, **options):
        message: str = 'You are about to make changes to the db.'

        if options['cleanphotos']:
            message = 'You are about to delete all photos not being used in media folder.'

        self.stdout.write(message)
        self.stdout.write('Type Y to proceed, or any other key to cancel:')
        confirm = input().strip().upper()
        if confirm != 'Y':
            self.stdout.write('Operation canceled.')
            return

        if options['ranking']:
            self.check_ranking()
        elif options['matchcount']:
            self.update_match_counts()
        elif options['cleanphotos']:
            self.clean_photos()
        else:
            self.stdout.write('No action specified. Usage: python manage.py check_integrity [options]')
            self.stdout.write('Options:')
            self.stdout.write('--ranking: Check and update player rankings')
            self.stdout.write('--matchcount: Update match counts for each player')
            self.stdout.write('--cleanphotos: Delete all players photos not being used in media folder')

    def check_ranking(self):
        """
        For efficiency iterate over all matches and keep adding points to the player's ranking, setting all to zero first
        :return:
        """
        self.stdout.write('Checking player rankings...')
        # All players to zero
        for player in Player.objects.all():
            player.ranking = 0
            player.save()

        for single_match in SinglesMatch.objects.all():
            winner = single_match.winner
            if winner:
                winner.add_points(WINNING_POINTS)

        for doubles_match in DoublesMatch.objects.all():
            winners = doubles_match.winners
            if winners:
                for winner in winners:
                    winner.add_points(WINNING_POINTS)




        # for player in Player.objects.all():
        #     calculated_ranking = 0
        #     singles_matches = SinglesMatch.objects.all()
        #     for match in singles_matches:
        #         if player not in match.players:
        #             continue
        #         if player != match.winner:
        #             calculated_ranking -= LOSING_POINTS
        #             continue
        #         calculated_ranking += WINNING_POINTS
        #
        #     doubles_matches = DoublesMatch.objects.all()
        #     for match in doubles_matches:
        #         if player not in match.players:
        #             continue
        #         if player not in match.winners:
        #             calculated_ranking -= LOSING_POINTS
        #             continue
        #         calculated_ranking += WINNING_POINTS
        #
        #     if calculated_ranking != player.ranking:
        #         self.stdout.write(
        #             f"Discrepancy found for {player}: expected {calculated_ranking}, found {player.ranking}")
        #         player.ranking = calculated_ranking
        #         player.save()

        self.stdout.write('Ranking checked')

    def update_match_counts(self):
        self.stdout.write('Updating match counts for players...')
        for player in Player.objects.all():
            singles_match_count = SinglesMatch.objects.filter(
                player1=player
            ).count() + SinglesMatch.objects.filter(
                player2=player
            ).count()

            doubles_match_count = DoublesMatch.objects.filter(
                team1_player1=player
            ).count() + DoublesMatch.objects.filter(
                team1_player2=player
            ).count() + DoublesMatch.objects.filter(
                team2_player1=player
            ).count() + DoublesMatch.objects.filter(
                team2_player2=player
            ).count()

            total_match_count = singles_match_count + doubles_match_count

            if total_match_count != player.matches_played:
                self.stdout.write(
                    f"Discrepancy found for {player}: expected {total_match_count}, found {player.matches_played}"
                )

                player.matches_played = total_match_count
                player.save()
        self.stdout.write('Match counts checked')

    def clean_photos(self):
        self.stdout.write('Cleaning photos...')

        # Collect all used photos
        used_photos = set(Player.objects.values_list('photo', flat=True))
        used_photos = {os.path.basename(photo) for photo in used_photos if photo}  # Extract only the filenames

        # Path to the directory where photos are stored
        media_folder = os.path.join(settings.MEDIA_ROOT, 'player_photos')

        # List all files in the media folder
        all_photos = set(os.listdir(media_folder))

        # Calculate the difference
        unused_photos = all_photos - used_photos

        # Delete unused photos
        for photo in unused_photos:
            photo_path = os.path.join(media_folder, photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
                self.stdout.write(f'Removed unused photo: {photo}')

        self.stdout.write('Unused photos cleaned')

    def correct_season(self):
        self.stdout.write('Correcting season...')
        for single_match in SinglesMatch.objects.all():
            single_match.save()
        for doubles_match in DoublesMatch.objects.all():
            doubles_match.save()