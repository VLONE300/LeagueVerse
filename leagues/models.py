from django.db import models


# Create your models here.
class ConferenceStandings(models.Model):
    wins = models.IntegerField(default=0, verbose_name="Wins")
    losses = models.IntegerField(default=0, verbose_name="Losses")
    home = models.CharField(max_length=10, verbose_name="Home Record")
    away = models.CharField(max_length=10, verbose_name="Away Record")
    last_ten_games = models.CharField(max_length=10, verbose_name="Last 10 Games")
    streak = models.CharField(max_length=10, verbose_name="Current Streak")


class NBAStandings(ConferenceStandings):
    pct = models.FloatField(verbose_name='Winning Percentage')
    gb = models.FloatField(verbose_name='Games Back')
    ppg = models.FloatField(verbose_name='Points Percentage Game')
    oop_ppg = models.FloatField(verbose_name='Opponent Points Percentage Game')
    conf = models.CharField(verbose_name='Conference Record')
    div = models.CharField(verbose_name='Division Record')


class NHLStandings(ConferenceStandings):
    otl = models.IntegerField(verbose_name='Number of Overtime Losses')
    row = models.IntegerField(verbose_name='Number of Regulation and Overtime Wins')
    sow = models.IntegerField(verbose_name='Shootout Wins')
    sol = models.IntegerField(verbose_name='Shootout Losses')
    gf = models.IntegerField(verbose_name='Goals For')
    ga = models.IntegerField(verbose_name='Goals Against')
    gd = models.IntegerField(verbose_name='Goal Differential')
