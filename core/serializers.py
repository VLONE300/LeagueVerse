from rest_framework import serializers

from core.models import League
from nba.serializers import NBATeamsSerializer
from nhl.serializers import NHLTeamsSerializer
from users.models import FavoriteTeam


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'logo')


class FavoriteTeamSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteTeam
        fields = ('id', 'team')

    def get_team(self, obj):
        if obj.content_type.model == 'nbateam':
            return NBATeamsSerializer(obj.content_object).data
        elif obj.content_type.model == 'nhlteam':
            return NHLTeamsSerializer(obj.content_object).data
        return None
