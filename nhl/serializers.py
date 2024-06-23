from rest_framework import serializers

from nhl.models import NHLStanding, NHLTeam, NHLGame, NHLTeamStats, NHLBoxScore


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


class NBAGameStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NHLTeamStats
        fields = '__all__'


class NHLBoxScoreSerializer(serializers.ModelSerializer):
    visitor_team_stats = NBAGameStatsSerializer()
    home_team_stats = NBAGameStatsSerializer()

    class Meta:
        model = NHLBoxScore
        fields = '__all__'


class NHLGameListSerializer(serializers.ModelSerializer):
    visitor_team = NHLTeamsSerializer()
    home_team = NHLTeamsSerializer()

    class Meta:
        model = NHLGame
        fields = ('id', 'date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts',)

    def get_visitor_team(self, obj):
        return obj.visitor_team.name

    def get_home_team(self, obj):
        return obj.home_team.name


class NHLGameDetailSerializer(serializers.ModelSerializer):
    box_score = NHLBoxScoreSerializer()
    visitor_team = NHLTeamsSerializer()
    home_team = NHLTeamsSerializer()

    class Meta:
        model = NHLGame
        fields = (
            'date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'time', 'status', 'arena', 'type',
            'box_score')

    def get_visitor_team(self, obj):
        return obj.visitor_team.name

    def get_home_team(self, obj):
        return obj.home_team.name


class NBAScheduleSerializer(NHLGameListSerializer):
    class Meta:
        model = NHLGame
        fields = NHLGameListSerializer.Meta.fields + ('time', 'arena', 'type')
