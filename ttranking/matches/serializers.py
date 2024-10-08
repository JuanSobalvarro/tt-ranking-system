# ttranking/matches/serializers.py
from rest_framework import serializers
from .models import SinglesMatch, DoublesMatch


class SinglesMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinglesMatch
        fields = '__all__'


class DoublesMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoublesMatch
        fields = '__all__'

