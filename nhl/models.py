from django.db import models
from core.models import Team, ConferenceStanding


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


class NHLGame(models.Model):
    STATUS_GAME = (
        ('finished', 'Finished'),
        ('waiting', 'Waiting'),
    )

    visitor_team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, related_name='visitor_games')
    visitor_pts = models.CharField(max_length=10)
    home_team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, related_name='home_games')
    home_pts = models.CharField(max_length=10)
    date = models.DateField()
    box_score_link = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(choices=STATUS_GAME, max_length=10)
    overtime = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "NHL Game"
        verbose_name_plural = "NHL Games"
