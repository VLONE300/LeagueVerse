from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from nhl.models import NHLTeam, NHLStanding
from nhl.serializers import NHLTeamsSerializer, NHLStandingsSerializer


class NHLTeamsView(ReadOnlyModelViewSet):
    queryset = NHLTeam.objects.all()
    serializer_class = NHLTeamsSerializer


class NHLStandingsView(ReadOnlyModelViewSet):
    serializer_class = NHLStandingsSerializer
    queryset = NHLStanding.objects.all()

