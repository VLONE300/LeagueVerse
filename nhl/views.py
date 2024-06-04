
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.views import StandingsView, GamesView
from nhl.models import NHLTeam, NHLStanding, NHLGame
from nhl.serializers import NHLTeamsSerializer, NHLStandingsSerializer, NHLGamesSerializer


class NHLTeamsView(ReadOnlyModelViewSet):
    queryset = NHLTeam.objects.all()
    serializer_class = NHLTeamsSerializer


class NHLStandingsView(StandingsView):
    serializer_class = NHLStandingsSerializer
    queryset = NHLStanding.objects.all()


class NHLScoresView(GamesView):
    queryset = NHLGame.objects.filter(status='Finished').order_by('-date')
    serializer_class = NHLGamesSerializer


class NHLScheduleView(GamesView):
    queryset = NHLGame.objects.filter(status='Waiting').order_by('-date')
    serializer_class = NHLGamesSerializer
