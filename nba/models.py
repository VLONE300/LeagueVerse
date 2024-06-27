from django.db import models
from core.models import Team, ConferenceStanding, Game


class NBATeam(Team):
    team_logo = models.ImageField(upload_to="logos/nba", null=True, blank=True)

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
    field_goals = models.IntegerField(blank=True, null=True)
    field_goal_attempts = models.IntegerField(blank=True, null=True)
    field_goals_percentage = models.FloatField(blank=True, null=True)
    three_point_field_goals = models.IntegerField(blank=True, null=True)
    three_point_field_goal_attempts = models.IntegerField(blank=True, null=True)
    three_point_field_goals_percentage = models.FloatField(blank=True, null=True)
    free_throws = models.IntegerField(blank=True, null=True)
    free_throw_attempts = models.IntegerField(blank=True, null=True)
    free_throw_percentage = models.FloatField(blank=True, null=True)
    personal_fouls = models.IntegerField(blank=True, null=True)
    total_rebounds = models.IntegerField(blank=True, null=True)
    offensive_rebounds = models.IntegerField(blank=True, null=True)
    turnovers = models.IntegerField(blank=True, null=True)
    assists = models.IntegerField(blank=True, null=True)
    steals = models.IntegerField(blank=True, null=True)
    blocks = models.IntegerField(blank=True, null=True)
