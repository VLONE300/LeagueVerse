from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from leagues.models import League, NBATeams, NHLTeams
from leagues.serializers import LeagueSerializer, TeamsSerializer, NBTeamsSerializer, NHLTeamsSerializer


class LeagueView(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class TeamsView(ReadOnlyModelViewSet):
    serializer_class = TeamsSerializer


class NBATeamsView(TeamsView):
    queryset = NBATeams.objects.all()
    serializer_class = NBTeamsSerializer


class NHLTeamsView(TeamsView):
    queryset = NHLTeams.objects.all()
    serializer_class = NHLTeamsSerializer
