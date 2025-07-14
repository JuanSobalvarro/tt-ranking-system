from rest_framework import serializers
from .models import Season

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'name', 'start_date', 'end_date', 'singles_points_for_win', 'singles_points_for_loss',
                  'doubles_points_for_win', 'doubles_points_for_loss']

