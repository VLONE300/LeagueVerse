from rest_framework import serializers

from nba.models import NBAStanding, NBATeam, NBAGame


class NBATeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBATeam
        fields = ('id', 'name', 'conference', 'division', 'team_logo')


class NBAStandingsSerializer(serializers.ModelSerializer):
    team = NBATeamsSerializer()

    class Meta:
        model = NBAStanding
        fields = ('team', 'wins', 'losses', 'winning_percentage', 'points_percentage_game', 'games_back',
                  'oop_points_percentage_game',)


class NBAGamesSerializer(serializers.ModelSerializer):
    visitor_team = NBATeamsSerializer()
    home_team = NBATeamsSerializer()

    class Meta:
        model = NBAGame
        fields = ('date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'status')

    def get_visitor_team(self, obj):
        return obj.visitor_team.name

    def get_home_team(self, obj):
        return obj.home_team.name
