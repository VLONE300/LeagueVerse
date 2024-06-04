from django.db import models
from core.models import Team, ConferenceStanding, Game


class NBATeam(Team):
    team_logo = models.ImageField(upload_to="logos/nba")

    class Meta:
        verbose_name = "NBA Team"
        verbose_name_plural = "NBA Teams"

    def __str__(self):
        return self.name


class NBAStanding(ConferenceStanding):
    team = models.ForeignKey(NBATeam, on_delete=models.CASCADE)
    winning_percentage = models.FloatField()
    games_back = models.CharField(max_length=10)
    points_percentage_game = models.FloatField()
    oop_points_percentage_game = models.FloatField()


class NBAGame(Game):
    visitor_team = models.ForeignKey(NBATeam, on_delete=models.CASCADE, related_name='visitor_games')
    home_team = models.ForeignKey(NBATeam, on_delete=models.CASCADE, related_name='home_games')

    class Meta:
        verbose_name = "NBA Game"
        verbose_name_plural = "NBA Games"

    def __str__(self):
        return f'{self.date} {self.visitor_team} - {self.home_team}'
