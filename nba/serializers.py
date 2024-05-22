from rest_framework import serializers

from nba.models import NBAStanding, NBATeam


class NBATeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBATeam
        fields = ('id', 'name', 'conference', 'division')


class NBAStandingsSerializer(serializers.ModelSerializer):
    team = NBATeamsSerializer()

    class Meta:
        model = NBAStanding
        fields = ('team', 'wins', 'losses', 'winning_percentage', 'points_percentage_game', 'games_back',
                  'oop_points_percentage_game',)
