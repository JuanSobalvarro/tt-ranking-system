# ttranking/matches/serializers.py
from rest_framework import serializers
from .models import SinglesMatch, DoublesMatch, SinglesGame, DoublesGame

class SinglesGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinglesGame
        fields = '__all__'

class DoublesGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoublesGame
        fields = '__all__'

class SinglesMatchSerializer(serializers.ModelSerializer):
    player1_games = serializers.SerializerMethodField()
    player2_games = serializers.SerializerMethodField()

    class Meta:
        model = SinglesMatch
        fields = '__all__'

    def get_player1_games(self, obj):
        return obj.games_won[0]

    def get_player2_games(self, obj):
        return obj.games_won[1]

class DoublesMatchSerializer(serializers.ModelSerializer):
    team1_games = serializers.SerializerMethodField()
    team2_games = serializers.SerializerMethodField()

    class Meta:
        model = DoublesMatch
        fields = '__all__'

    def get_team1_games(self, obj):
        return obj.games_won[0]

    def get_team2_games(self, obj):
        return obj.games_won[1]
