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
    CONFERENCE = (
        ('Eastern', 'Eastern'),
        ('Western', 'Western'),
    )

    name = models.CharField(max_length=255)
    conference = models.CharField(choices=CONFERENCE, max_length=10)
    division = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class NBATeams(Teams):
    class Meta:
        verbose_name = "NBA Team"
        verbose_name_plural = "NBA Teams"


class NHLTeams(Teams):
    class Meta:
        verbose_name = "NHL Team"
        verbose_name_plural = "NHL Teams"


class ConferenceStandings(models.Model):
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    # home_record = models.CharField(max_length=10)
    # away_record = models.CharField(max_length=10)
    # last_ten_games = models.CharField(max_length=10)
    # streak = models.CharField(max_length=10)

    class Meta:
        abstract = True


class NBAStandings(ConferenceStandings):
    team = models.ForeignKey(NBATeams, on_delete=models.CASCADE)
    winning_percentage = models.FloatField()
    games_back = models.CharField(max_length=10)
    points_percentage_game = models.FloatField()
    oop_points_percentage_game = models.FloatField()
    # conference_record = models.CharField(max_length=10)
    # division_record = models.CharField(max_length=10)


class NHLStandings(ConferenceStandings):
    team = models.ForeignKey(NHLTeams, on_delete=models.CASCADE)
    num_of_overtime_losses = models.IntegerField()
    num_of_regulation_and_overtime_wins = models.IntegerField()
    shootout_wins = models.IntegerField()
    shootout_losses = models.IntegerField()
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    goal_differential = models.IntegerField()
