from django.db import models

from core.utils import nba_slug_team_name


class League(models.Model):
    name = models.CharField(max_length=55)
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "League"
        verbose_name_plural = "Leagues"


class Team(models.Model):
    name = models.CharField(max_length=255)
    conference = models.CharField(max_length=255)
    division = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ConferenceStanding(models.Model):
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Game(models.Model):
    STATUS_GAME = (
        ('finished', 'Finished'),
        ('waiting', 'Waiting'),
    )
    TYPE_GAME = (
        ('regular season', 'Regular Season'),
        ('playoff', 'Playoff'),
    )
    visitor_pts = models.IntegerField(blank=True, null=True)
    home_pts = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    time = models.CharField(max_length=20, blank=True)
    status = models.CharField(choices=STATUS_GAME, max_length=10)
    arena = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        date_part = str(self.date).replace('-', '')
        if hasattr(self, 'visitor_team'):
            if self.visitor_team.name in nba_slug_team_name:
                visitor_team_slug = nba_slug_team_name[self.visitor_team.name]
                self.slug = f"{date_part}-{visitor_team_slug}"
            else:
                raise ValueError(f"Unknown NBA team name: {self.visitor_team.name}")

    class Meta:
        abstract = True
