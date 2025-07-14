# ttranking/matches/admin.py
from django.contrib import admin
from .models import SinglesMatch, DoublesMatch, SinglesGame, DoublesGame

admin.site.register(SinglesGame)
admin.site.register(DoublesGame)
admin.site.register(SinglesMatch)
admin.site.register(DoublesMatch)

