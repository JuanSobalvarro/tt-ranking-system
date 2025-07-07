from rest_framework import serializers
from .models import Player, Ranking


class PlayerSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)  # Make the id field optional
    photo = serializers.ImageField(required=False)  # Make the photo field optional

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'alias', 'gender', 'date_of_birth',
                  'nationality', 'photo', 'created_at', 'updated_at']

class RankingSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.IntegerField(source='player.id', write_only=True)
    ranking = serializers.IntegerField(read_only=True)
    singles_matches_played = serializers.IntegerField(read_only=True)
    doubles_matches_played = serializers.IntegerField(read_only=True)
    singles_victories = serializers.IntegerField(read_only=True)
    doubles_victories = serializers.IntegerField(read_only=True)

    victories = serializers.SerializerMethodField(read_only=True)
    matches_played = serializers.SerializerMethodField(read_only=True)
    winrate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ranking
        fields = ['id', 'player', 'player_id', 'season', 'ranking', 'singles_matches_played',
                  'doubles_matches_played', 'singles_victories', 'doubles_victories', 'victories',
                  'matches_played', 'winrate']

    def get_winrate(self, obj):
        return obj.winrate

    def get_player(self, obj):
        return obj.player

    def get_victories(self, obj):
        return obj.victories

    def get_matches_played(self, obj):
        return obj.matches_played
