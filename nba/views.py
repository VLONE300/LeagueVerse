from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.views import StandingsView, GamesView
from nba.models import NBAStanding, NBATeam, NBAGame
from nba import serializers
from nba.utils import get_stats


class NBATeamsView(ReadOnlyModelViewSet):
    queryset = NBATeam.objects.all()
    serializer_class = serializers.NBATeamsSerializer


class NBAStandingsView(StandingsView):
    queryset = NBAStanding.objects.all()
    serializer_class = serializers.NBAStandingsSerializer


class NBAScoreView(GamesView):
    queryset = NBAGame.objects.all().order_by('-date')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.NBAGameDetailSerializer
        return serializers.NBAGameListSerializer


class NBAScheduleView(GamesView):
    queryset = NBAGame.objects.all().order_by('-date')
    serializer_class = serializers.NBAScheduleSerializer


class NBAGamesDateView(ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        return Response([i.date for i in NBAGame.objects.all()])


#  slug = date_str+game.home_team.name.upper()[:3]

class NBATeamStatsView(ReadOnlyModelViewSet):
    serializer_class = serializers.NBATeamStatsSerializer

    def list(self, request, *args, **kwargs):
        teams = NBATeam.objects.all()
        team_stats = get_stats(teams)
        return Response(team_stats)
