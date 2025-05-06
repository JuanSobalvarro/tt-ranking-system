# ttranking/players/management/commands/create_periodic_task.py
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Create or update the periodic task for server integrity check.'

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=24,
            period=IntervalSchedule.SECONDS,
        )

        try:
            task = PeriodicTask.objects.get(name='server-integrity-check')
            task.interval = schedule
            task.task = 'core.tasks.check_server_integrity'
            task.save()
            self.stdout.write(self.style.SUCCESS('Updated the periodic task.'))
        except ObjectDoesNotExist:
            PeriodicTask.objects.create(
                interval=schedule,
                name='server-integrity-check',
                task='core.tasks.check_server_integrity',
            )
            self.stdout.write(self.style.SUCCESS('Created a new periodic task.'))
