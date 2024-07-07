from rest_framework import serializers

from nhl.models import NHLStanding, NHLTeam, NHLGame, NHLTeamStats, NHLBoxScore
from nhl.utils import get_nhl_box_score


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
    stats = serializers.SerializerMethodField()

    class Meta:
        model = NHLBoxScore
        fields = ['stats']

    def get_stats(self, obj):
        stats = get_nhl_box_score(obj)
        return stats


class NHLGameListSerializer(serializers.ModelSerializer):
    visitor_team = NHLTeamsSerializer()
    home_team = NHLTeamsSerializer()

    class Meta:
        model = NHLGame
        fields = ('id', 'date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'slug')


class NHLGameDetailSerializer(serializers.ModelSerializer):
    box_score = NHLBoxScoreSerializer()
    visitor_team = NHLTeamsSerializer()
    home_team = NHLTeamsSerializer()

    class Meta:
        model = NHLGame
        fields = (
            'date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'time', 'status', 'arena', 'type',
            'box_score')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        box_score_data = representation.pop('box_score')['stats']
        representation['box_score'] = box_score_data
        return representation


class NHLScheduleSerializer(NHLGameListSerializer):
    class Meta:
        model = NHLGame
        fields = NHLGameListSerializer.Meta.fields + ('time', 'arena', 'type')


class DateGamesSerializer(serializers.Serializer):
    date = serializers.DateField()
    games = NHLScheduleSerializer(many=True)


class NHLTeamStatsSerializer(serializers.Serializer):
    team = NHLTeamsSerializer()
    avg_points_per_game = serializers.FloatField()

    def get_team(self, obj):
        return obj.team.name
