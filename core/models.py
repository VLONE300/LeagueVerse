from django.db import models

from django.db import models


class League(models.Model):
    name = models.CharField(max_length=55)
    sport = models.CharField(max_length=100)

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
