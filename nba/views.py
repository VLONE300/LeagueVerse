from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.views import StandingsView, GamesView
from nba.models import NBAStanding, NBATeam, NBAGame
from nba import serializers
from nba.utils import get_nba_stats


class NBATeamsView(ReadOnlyModelViewSet):
    queryset = NBATeam.objects.all()
    serializer_class = serializers.NBATeamSerializer


class NBAStandingsView(StandingsView):
    queryset = NBAStanding.objects.all().order_by('-winning_percentage')
    serializer_class = serializers.NBAStandingsSerializer


class NBAScoreView(GamesView):
    queryset = NBAGame.objects.all().order_by('-date')
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.NBAGameDetailSerializer
        return serializers.NBAGameListSerializer


class NBAScheduleView(GamesView):
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        return self.list_schedule(NBAGame, serializers.DateGamesSerializer, request)


class NBAGamesDateView(GamesView):
    def list(self, request, *args, **kwargs):
        return self.list_game_dates(NBAGame)


class NBATeamStatsView(ReadOnlyModelViewSet):
    serializer_class = serializers.NBATeamStatsSerializer

    def list(self, request, *args, **kwargs):
        teams = NBATeam.objects.all()
        team_stats = get_nba_stats(teams)
        return Response(team_stats)
