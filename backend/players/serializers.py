from rest_framework import serializers
from .models import Player, Ranking


class PlayerSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)  # Make the id field optional
    photo = serializers.ImageField(required=False)  # Make the photo field optional

    class Meta:
        model = Player
        fields = '__all__'  # or specify fields explicitly like ['id', 'name', 'age', 'team']

class RankingSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    winrate = serializers.SerializerMethodField(read_only=True)
    victories = serializers.SerializerMethodField(read_only=True)
    matches_played = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ranking
        fields = '__all__'

    def get_winrate(self, obj):
        return obj.winrate

    def get_player(self, obj):
        return obj.player

    def get_victories(self, obj):
        return obj.victories

    def get_matches_played(self, obj):
        return obj.matches_played
