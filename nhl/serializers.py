from rest_framework import serializers

from nhl.models import NHLStanding, NHLTeam


class NHLTeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NHLTeam
        fields = ('id', 'name', 'conference', 'division', 'team_logo')


class NHLStandingsSerializer(serializers.ModelSerializer):
    team = NHLTeamsSerializer()

    class Meta:
        model = NHLStanding
        fields = ('team', 'wins', 'losses', 'games_played', 'num_of_overtime_losses', 'total_points',
                  'points_percentage', 'goals_for', 'goals_against', 'wins_of_regulation')
