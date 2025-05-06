from django import forms
import datetime
from django.utils.translation import gettext_lazy as _
from .models import SinglesMatch, DoublesMatch
from players.models import Player

class SinglesMatchForm(forms.ModelForm):
    class Meta:
        model = SinglesMatch
        fields = ['date', 'player1', 'player1_score', 'player2', 'player2_score']
        labels = {
            'date': _('Fecha y hora'),
            'player1': _('Jugador 1'),
            'player1_score': _('Puntos de Jugador 1'),
            'player2': _('Jugador 2'),
            'player2_score': _('Puntos de Jugador 2'),
        }
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'type': 'datetime-local'}),
            'player1': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'player1_score': forms.NumberInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'player2': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'player2_score': forms.NumberInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }

    def set_labels(self):
        for field, label in zip(self.fields, self.labels):
            field.label = label

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.datetime.now().replace(second=0, microsecond=0)
        self.fields['player1'].queryset = Player.objects.all().order_by('first_name')
        self.fields['player2'].queryset = Player.objects.all().order_by('first_name')

    def clean(self):
        cleaned_data = super().clean()
        player1 = cleaned_data.get('player1')
        player2 = cleaned_data.get('player2')

        if player1 == player2:
            raise forms.ValidationError("Player 1 and Player 2 cannot be the same.")

        return cleaned_data

class DoublesMatchForm(forms.ModelForm):
    class Meta:
        model = DoublesMatch
        fields = ['date', 'team1_player1', 'team1_player2', 'team1_score', 'team2_player1', 'team2_player2', 'team2_score']
        labels = {
            'date': _('Fecha y hora'),
            'team1_player1': _('Equipo 1, jugador 1'),
            'team1_player2': _('Equipo 1, jugador 2'),
            'team1_score': _('Puntos del Equipo 1'),
            'team2_player1': _('Equipo 2, jugador 1'),
            'team2_player2': _('Equipo 2, jugador 2'),
            'team2_score': _('Puntos del Equipo 2'),
        }
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'type': 'datetime-local'}),
            'team1_player1': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'team1_player2': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'team1_score': forms.NumberInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'team2_player1': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'team2_player2': forms.Select(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'team2_score': forms.NumberInput(attrs={'class': 'form-control block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.datetime.now().replace(second=0, microsecond=0)
        self.fields['team1_player1'].queryset = Player.objects.all().order_by('first_name')
        self.fields['team1_player2'].queryset = Player.objects.all().order_by('first_name')
        self.fields['team2_player1'].queryset = Player.objects.all().order_by('first_name')
        self.fields['team2_player2'].queryset = Player.objects.all().order_by('first_name')

    def clean(self):
        cleaned_data = super().clean()
        team1_player1 = cleaned_data.get('team1_player1')
        team1_player2 = cleaned_data.get('team1_player2')
        team2_player1 = cleaned_data.get('team2_player1')
        team2_player2 = cleaned_data.get('team2_player2')

        if team1_player1 == team1_player2:
            raise forms.ValidationError("Team 1 players cannot be the same.")
        if team2_player1 == team2_player2:
            raise forms.ValidationError("Team 2 players cannot be the same.")
        all_players = {team1_player1, team1_player2, team2_player1, team2_player2}
        if len(all_players) < 4:
            raise forms.ValidationError("Players cannot be repeated across teams.")

        return cleaned_data