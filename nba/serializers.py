from rest_framework import serializers

from nba.models import NBAStanding, NBATeam, NBAGame, NBATeamStats, NBABoxScore


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


class NBATeamStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBATeamStats
        fields = '__all__'


class NBABoxScoreSerializer(serializers.ModelSerializer):
    home_team_stats = NBATeamStatsSerializer()
    visitor_team_stats = NBATeamStatsSerializer()

    class Meta:
        model = NBABoxScore
        fields = '__all__'


class NBAGameListSerializer(serializers.ModelSerializer):
    visitor_team = NBATeamsSerializer()
    home_team = NBATeamsSerializer()

    class Meta:
        model = NBAGame
        fields = ('date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts',)

    def get_visitor_team(self, obj):
        return obj.visitor_team.name

    def get_home_team(self, obj):
        return obj.home_team.name


class NBAGameDetailSerializer(serializers.ModelSerializer):
    box_score = NBABoxScoreSerializer()
    visitor_team = NBATeamsSerializer()
    home_team = NBATeamsSerializer()

    class Meta:
        model = NBAGame
        fields = (
            'date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'time', 'status', 'arena', 'type',
            'box_score')

    def get_visitor_team(self, obj):
        return obj.visitor_team.name

    def get_home_team(self, obj):
        return obj.home_team.name


class NBAScheduleSerializer(NBAGameListSerializer):
    class Meta:
        model = NBAGame
        fields = NBAGameListSerializer.Meta.fields + ('time', 'arena')


class NBAGamesDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBAGame
        fields = ('date',)



