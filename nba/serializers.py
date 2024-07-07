from rest_framework import serializers
from nba.models import NBAStanding, NBATeam, NBAGame, NBATeamStats, NBABoxScore
from nba.utils import get_nba_box_score


class NBATeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBATeam
        fields = ('id', 'name', 'conference', 'division', 'team_logo')


class NBAStandingsSerializer(serializers.ModelSerializer):
    team = NBATeamSerializer()

    class Meta:
        model = NBAStanding
        fields = ('team', 'wins', 'losses', 'winning_percentage', 'points_percentage_game', 'games_back',
                  'oop_points_percentage_game',)


class NBAGameStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NBATeamStats
        fields = '__all__'


class NBAGameListSerializer(serializers.ModelSerializer):
    visitor_team = NBATeamSerializer()
    home_team = NBATeamSerializer()

    class Meta:
        model = NBAGame
        fields = ('id', 'date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'slug')


class NBABoxScoreSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()

    class Meta:
        model = NBABoxScore
        fields = ['stats']

    def get_stats(self, obj):
        stats = get_nba_box_score(obj)
        return stats


class NBAGameDetailSerializer(serializers.ModelSerializer):
    box_score = NBABoxScoreSerializer()
    visitor_team = NBATeamSerializer()
    home_team = NBATeamSerializer()

    class Meta:
        model = NBAGame
        fields = (
            'date', 'visitor_team', 'visitor_pts', 'home_team', 'home_pts', 'time', 'status', 'arena', 'type',
            'box_score')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        box_score_data = representation.pop('box_score')['stats']
        representation['box_score'] = box_score_data
        return representation


class NBAScheduleSerializer(NBAGameListSerializer):
    class Meta:
        model = NBAGame
        fields = NBAGameListSerializer.Meta.fields + ('time', 'arena', 'type')


class DateGamesSerializer(serializers.Serializer):
    date = serializers.DateField()
    games = NBAScheduleSerializer(many=True)


class NBATeamStatsSerializer(serializers.Serializer):
    team = NBATeamSerializer()
    avg_points_per_game = serializers.FloatField()
