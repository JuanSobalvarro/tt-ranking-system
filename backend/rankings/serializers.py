from rest_framework import serializers
from .models import Ranking
from profiles.serializers import PlayerProfileSerializer
from profiles.models import PlayerProfile

class RankingSerializer(serializers.ModelSerializer):
    # player = PlayerProfileSerializer(source='player_profile', read_only=True)
    player_id = serializers.IntegerField(source='player_profile.id')

    class Meta:
        model = Ranking
        fields = ['id', 'player_id', 'season', 'ranking', 'singles_matches_played', 'doubles_matches_played',
                  'doubles_victories', 'singles_victories', 'matches_played', 'victories', 'winrate']

    def get_victories(self, obj):
        return obj.victories

    def get_matches_played(self, obj):
        return obj.matches_played

    def get_winrate(self, obj):
        return obj.winrate
