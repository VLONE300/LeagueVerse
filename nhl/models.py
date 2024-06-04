from django.db import models
from core.models import Team, ConferenceStanding, Game


class NHLTeam(Team):
    team_logo = models.ImageField(upload_to="logos/nhl")

    class Meta:
        verbose_name = "NHL Team"
        verbose_name_plural = "NHL Teams"


class NHLStanding(ConferenceStanding):
    team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    games_played = models.IntegerField()
    num_of_overtime_losses = models.IntegerField()
    total_points = models.IntegerField()
    points_percentage = models.FloatField()
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    wins_of_regulation = models.IntegerField()


class NHLGame(Game):
    visitor_team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, related_name='visitor_games')
    home_team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, related_name='home_games')
    overtime = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "NHL Game"
        verbose_name_plural = "NHL Games"

    def __str__(self):
        return f'{self.date} {self.visitor_team} - {self.home_team}'
