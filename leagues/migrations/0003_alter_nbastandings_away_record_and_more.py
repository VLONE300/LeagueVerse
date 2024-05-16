# Generated by Django 5.0.6 on 2024-05-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0002_alter_nbateams_conference_alter_nhlteams_conference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nbastandings',
            name='away_record',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='conference_record',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='division_record',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='games_back',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='home_record',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='last_ten_games',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='oop_points_percentage_game',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='points_percentage_game',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='streak',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='winning_percentage',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='nbastandings',
            name='wins',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='away_record',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='goal_differential',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='goals_against',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='goals_for',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='home_record',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='last_ten_games',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='num_of_overtime_losses',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='num_of_regulation_and_overtime_wins',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='shootout_losses',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='shootout_wins',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='streak',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='nhlstandings',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
