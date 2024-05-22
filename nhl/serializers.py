from rest_framework import serializers

from nhl.models import NHLStanding, NHLTeam


class NBATeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NHLTeam
        fields = ('id', 'name', 'conference', 'division')


class NBAStandingsSerializer(serializers.ModelSerializer):
    team = NBATeamsSerializer()

    class Meta:
        model = NHLStanding
        fields = ('team', 'wins', 'losses', 'winning_percentage', 'points_percentage_game', 'games_back',
                  'oop_points_percentage_game',)
