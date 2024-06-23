from rest_framework import serializers

from core.models import League
from nba.serializers import NBATeamsSerializer
from nhl.serializers import NHLTeamsSerializer
from users.models import Favorite


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'logo')


class FavoriteSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ('id', 'item')

    def get_item(self, obj):
        if obj.content_type.model == 'nbateam':
            return NBATeamsSerializer(obj.content_object).data
        elif obj.content_type.model == 'nhlteam':
            return NHLTeamsSerializer(obj.content_object).data
        elif obj.content_type.model == 'league':
            return LeagueSerializer(obj.content_object).data
        return None
