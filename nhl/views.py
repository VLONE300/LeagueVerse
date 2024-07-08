from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.views import StandingsView, GamesView, TeamView
from nhl.models import NHLTeam, NHLStanding, NHLGame
from nhl import serializers
from nhl.utils import get_nhl_stats


class NHLTeamsView(TeamView):
    serializer_class = serializers.NHLTeamSerializer
    queryset = NHLTeam.objects.all()


class NHLStandingsView(StandingsView):
    serializer_class = serializers.NHLStandingsSerializer
    queryset = NHLStanding.objects.all().select_related('team').order_by('-wins')


class NHLScoreView(GamesView):
    queryset = NHLGame.objects.all().select_related('visitor_team').select_related('home_team').order_by('-date')
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.NHLGameDetailSerializer
        return serializers.NHLGameListSerializer


class NHLScheduleView(GamesView):
    serializer_class = serializers.NHLScheduleSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        return self.list_schedule(NHLGame, serializers.DateGamesSerializer, request)


class NHLGamesDateView(GamesView):
    def list(self, request, *args, **kwargs):
        return self.list_game_dates(NHLGame)


class NHLTeamStatsView(ReadOnlyModelViewSet):
    serializer_class = serializers.NHLTeamStatsSerializer

    def list(self, request, *args, **kwargs):
        teams = NHLTeam.objects.all()
        team_stats = get_nhl_stats(teams)
        return Response(team_stats)
