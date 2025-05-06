from datetime import datetime
from django.db import models


class Season(models.Model):
    """
    A season is a period of time during which matches are played.
    Fields: name, description, start_date, end_date, singles_points_for_win, singles_points_for_loss,
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    singles_points_for_win = models.IntegerField(default=2, blank=True)
    singles_points_for_loss = models.IntegerField(default=0, blank=True)
    doubles_points_for_win = models.IntegerField(default=1, blank=True)
    doubles_points_for_loss = models.IntegerField(default=0, blank=True)

    @staticmethod
    def get_season_for_datetime(dt: datetime) -> 'Season':
        """
        Returns the season for the given date. If the date is not within any season, returns None.
        :param date: The date (with or without time) to find the season for.
        :return: The season for the given date, or None if no season matches.
        """
        date_only = dt.date()
        return Season.objects.filter(start_date__lte=date_only, end_date__gte=date_only).first()

    def validate_date(self) -> bool:
        """
        Validates if the current date is within any season. If it overlaps with another season, it will raise an
        exception.
        :return:
        """
        print("Validating date for: ", self.start_date, self.end_date)
        if self.start_date > self.end_date:
            raise ValueError('Start date must be before end date')
        if Season.objects.filter(start_date__lte=self.start_date, end_date__gte=self.start_date).exclude(pk=self.pk).exists():
            raise ValueError('Start date overlaps with another season')
        if Season.objects.filter(start_date__lte=self.end_date, end_date__gte=self.end_date).exclude(pk=self.pk).exists():
            raise ValueError('End date overlaps with another season')
        return True

    def save(self, *args, **kwargs):
        self.validate_date()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
