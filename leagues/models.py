from django.db import models


class League(models.Model):
    name = models.CharField(max_length=55)
    sport = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "League"
        verbose_name_plural = "Leagues"


class Teams(models.Model):
    name = models.CharField(max_length=255)
    conference = models.CharField(max_length=255)
    division = models.CharField(max_length=255)

    class Meta:
        abstract = True


class NBATeams(Teams):
    class Meta:
        verbose_name = "NBA Team"
        verbose_name_plural = "NBA Teams"


class NHLTeams(Teams):
    class Meta:
        verbose_name = "NHL Team"
        verbose_name_plural = "NHL Teams"


class ConferenceStandings(models.Model):
    wins = models.IntegerField(default=0, verbose_name="Wins")
    losses = models.IntegerField(default=0, verbose_name="Losses")
    home_record = models.CharField(max_length=10, verbose_name="Home Record")
    away_record = models.CharField(max_length=10, verbose_name="Away Record")
    last_ten_games = models.CharField(max_length=10, verbose_name="Last 10 Games")
    streak = models.CharField(max_length=10, verbose_name="Current Streak")

    class Meta:
        abstract = True


class NBAStandings(ConferenceStandings):
    team = models.ForeignKey(NBATeams, on_delete=models.CASCADE)
    winning_percentage = models.FloatField(verbose_name='Winning Percentage')
    games_back = models.FloatField(verbose_name='Games Back')
    points_percentage_game = models.FloatField(verbose_name='Points Percentage Game')
    oop_points_percentage_game = models.FloatField(verbose_name='Opponent Points Percentage Game')
    conference_record = models.CharField(verbose_name='Conference Record')
    division_record = models.CharField(verbose_name='Division Record')


class NHLStandings(ConferenceStandings):
    team = models.ForeignKey(NHLTeams, on_delete=models.CASCADE)
    num_of_overtime_losses = models.IntegerField(verbose_name='Number of Overtime Losses')
    num_of_regulation_and_overtime_wins = models.IntegerField(verbose_name='Number of Regulation and Overtime Wins')
    shootout_wins = models.IntegerField(verbose_name='Shootout Wins')
    shootout_losses = models.IntegerField(verbose_name='Shootout Losses')
    goals_for = models.IntegerField(verbose_name='Goals For')
    goals_against = models.IntegerField(verbose_name='Goals Against')
    goal_differential = models.IntegerField(verbose_name='Goal Differential')
