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
    team = models.ForeignKey("NBATeam", on_delete=models.CASCADE)
    winning_percentage = models.FloatField()
    games_back = models.CharField(max_length=10)
    points_percentage_game = models.FloatField()
    oop_points_percentage_game = models.FloatField()


class NBAGame(Game):
    visitor_team = models.ForeignKey("NBATeam", on_delete=models.CASCADE, related_name="visitor_team")
    home_team = models.ForeignKey("NBATeam", on_delete=models.CASCADE, related_name="home_team")
    box_score = models.ForeignKey("NBABoxScore", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "NBA Game"
        verbose_name_plural = "NBA Games"

    def __str__(self):
        return f'{self.date} {self.visitor_team} - {self.home_team}'


class NBABoxScore(models.Model):
    home_team_stats = models.ForeignKey("NBATeamStats", on_delete=models.CASCADE, related_name="home_team_stats")
    visitor_team_stats = models.ForeignKey("NBATeamStats", on_delete=models.CASCADE, related_name="visitor_team_stats")


class NBATeamStats(models.Model):
    field_goals = models.IntegerField(default=0)
    field_goal_attempts = models.IntegerField(default=0)
    field_goals_percentage = models.FloatField(default=0.0)
    three_point_field_goals = models.IntegerField(default=0)
    three_point_field_goal_attempts = models.IntegerField(default=0)
    three_point_field_goals_percentage = models.FloatField(default=0.0)
    free_throws = models.IntegerField(default=0)
    free_throw_attempts = models.IntegerField(default=0)
    free_throw_percentage = models.FloatField(default=0.0)
    personal_fouls = models.IntegerField(default=0)
    total_rebounds = models.IntegerField(default=0)
    offensive_rebounds = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
