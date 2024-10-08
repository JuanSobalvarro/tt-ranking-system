# Generated by Django 5.0.7 on 2024-08-03 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_alter_player_nationality_alter_player_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='ranking',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
