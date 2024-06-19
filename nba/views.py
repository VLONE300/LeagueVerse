from rest_framework.viewsets import ReadOnlyModelViewSet
from core.views import StandingsView, GamesView
from nba.models import NBAStanding, NBATeam, NBAGame
from nba.serializers import NBATeamsSerializer, NBAStandingsSerializer, NBAGamesSerializer, NBAScheduleSerializer, \
    NBAGamesDateSerializer


class NBATeamsView(ReadOnlyModelViewSet):
    queryset = NBATeam.objects.all()
    serializer_class = NBATeamsSerializer


class NBAStandingsView(StandingsView):
    serializer_class = NBAStandingsSerializer
    queryset = NBAStanding.objects.all()


class NBAScoreView(GamesView):
    queryset = NBAGame.objects.filter(status='Finished').order_by('-date')
    serializer_class = NBAGamesSerializer


class NBAScheduleView(GamesView):
    queryset = NBAGame.objects.all()
    serializer_class = NBAScheduleSerializer


class NBAGamesDateView(ReadOnlyModelViewSet):
    queryset = NBAGame.objects.all()
    serializer_class = NBAGamesDateSerializer
