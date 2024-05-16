from rest_framework import serializers

from leagues.models import League, NBATeams, NHLTeams, NBAStandings


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name')


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'conference', 'division')


class NBATeamsSerializer(TeamsSerializer):
    class Meta(TeamsSerializer.Meta):
        model = NBATeams


class NHLTeamsSerializer(TeamsSerializer):
    class Meta(TeamsSerializer.Meta):
        model = NHLTeams


class NBAStandingsSerializer(serializers.ModelSerializer):
    team = NBATeamsSerializer()

    class Meta:
        model = NBAStandings
        fields = ('team', 'wins', 'losses', 'winning_percentage', 'points_percentage_game', 'games_back',
                  'oop_points_percentage_game',
                  'oop_points_percentage_game', 'home_record', 'conference_record', 'division_record', 'last_ten_games',
                  'streak')
