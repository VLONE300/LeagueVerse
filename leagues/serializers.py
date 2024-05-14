from rest_framework import serializers

from leagues.models import League, NBATeams, NHLTeams


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name')


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'conference', 'division')


class NBTeamsSerializer(TeamsSerializer):
    class Meta(TeamsSerializer.Meta):
        model = NBATeams


class NHLTeamsSerializer(TeamsSerializer):
    class Meta(TeamsSerializer.Meta):
        model = NHLTeams
