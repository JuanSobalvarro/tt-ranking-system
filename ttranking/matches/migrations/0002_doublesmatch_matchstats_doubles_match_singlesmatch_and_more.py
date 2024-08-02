# Generated by Django 5.0.7 on 2024-08-02 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoublesMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('score', models.CharField(max_length=20)),
                ('winner_team', models.CharField(blank=True, choices=[('Team1', 'Team 1'), ('Team2', 'Team 2')], max_length=10, null=True)),
                ('team1_player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doubles_matches_team1_player1', to='players.player')),
                ('team1_player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doubles_matches_team1_player2', to='players.player')),
                ('team2_player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doubles_matches_team2_player1', to='players.player')),
                ('team2_player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doubles_matches_team2_player2', to='players.player')),
            ],
        ),
        migrations.AddField(
            model_name='matchstats',
            name='doubles_match',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matches.doublesmatch'),
        ),
        migrations.CreateModel(
            name='SinglesMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('score', models.CharField(max_length=20)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='singles_matches_as_player1', to='players.player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='singles_matches_as_player2', to='players.player')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='singles_matches_won', to='players.player')),
            ],
        ),
        migrations.AlterField(
            model_name='matchstats',
            name='match',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='matches.singlesmatch'),
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]
