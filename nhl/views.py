from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.views import StandingsView, GamesView
from nhl.models import NHLTeam, NHLStanding, NHLGame
from nhl import serializers
from nhl.utils import get_nhl_stats


class NHLTeamsView(ReadOnlyModelViewSet):
    queryset = NHLTeam.objects.all()
    serializer_class = serializers.NHLTeamsSerializer


class NHLStandingsView(StandingsView):
    serializer_class = serializers.NHLStandingsSerializer
    queryset = NHLStanding.objects.all().order_by('-wins')


class NHLScoreView(GamesView):
    queryset = NHLGame.objects.all().order_by('-date')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.NHLGameDetailSerializer
        return serializers.NHLGameListSerializer


class NHLScheduleView(GamesView):
    queryset = NHLGame.objects.filter(status='Waiting').order_by('-date')
    serializer_class = serializers.NHLScheduleSerializer


class NHLGamesDateView(ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        return Response([i.date for i in NHLGame.objects.all()])


class NHLTeamStatsView(ReadOnlyModelViewSet):
    serializer_class = serializers.NHLTeamStatsSerializer

    def list(self, request, *args, **kwargs):
        teams = NHLTeam.objects.all()
        team_stats = get_nhl_stats(teams)
        return Response(team_stats)
