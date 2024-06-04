from rest_framework import serializers

from nhl.models import NHLStanding, NHLTeam, NHLGame


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


class NHLGamesSerializer(serializers.ModelSerializer):
    visitor_team = NHLTeamsSerializer()
    home_team = NHLTeamsSerializer()

    class Meta:
        model = NHLGame
        fields = ('date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'status', 'overtime', 'type')

    def get_visitor_team(self, obj):
        return obj.visitor_team.name

    def get_home_team(self, obj):
        return obj.home_team.name
