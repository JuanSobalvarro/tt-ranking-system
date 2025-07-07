# ttranking/matches/serializers.py
from rest_framework import serializers

from players.models import Player
from players.serializers import PlayerSerializer

from .models import SinglesMatch, DoublesMatch, SinglesGame, DoublesGame

class SinglesGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinglesGame
        fields = ['id', 'match', 'player1_score', 'player2_score', 'winner']

class DoublesGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoublesGame
        fields = '__all__'

class SinglesMatchSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S%z",
        input_formats=["%Y-%m-%dT%H:%M:%S%z"]
    )
    season_id = serializers.IntegerField(source='season.id', read_only=True)
    winner = serializers.IntegerField(source='winner.id', read_only=True)

    player1 = serializers.SerializerMethodField(read_only=True)
    player2 = serializers.SerializerMethodField(read_only=True)
    player1_id = serializers.IntegerField(write_only=True)
    player2_id = serializers.IntegerField(write_only=True)

    player1_wins = serializers.SerializerMethodField()
    player2_wins = serializers.SerializerMethodField()
    games = serializers.SerializerMethodField()

    class Meta:
        model = SinglesMatch
        fields = [
            'id', 'date', 'season_id', 'games',
            'player1', 'player1_id', 'player2', 'player2_id',
            'winner', 'player1_wins', 'player2_wins'
        ]

    def get_player1(self, obj):
        include_nested = self.context.get('include_nested', False)
        if include_nested:
            return PlayerSerializer(obj.player1).data
        return obj.player1.id

    def get_player2(self, obj):
        include_nested = self.context.get('include_nested', False)
        if include_nested:
            return PlayerSerializer(obj.player2).data
        return obj.player2.id

    def get_player1_wins(self, obj):
        return obj.games_won[0]

    def get_player2_wins(self, obj):
        return obj.games_won[1]

    def get_games(self, obj):
        include_nested = self.context.get('include_nested', False)
        if include_nested:
            return SinglesGameSerializer(obj.games, many=True).data
        return [game.id for game in obj.games.all()]


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
