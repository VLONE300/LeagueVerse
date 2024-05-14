from rest_framework import serializers

from leagues.models import League, NBATeams


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name')
