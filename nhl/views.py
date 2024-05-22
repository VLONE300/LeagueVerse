from rest_framework.viewsets import ReadOnlyModelViewSet

from nhl.models import NHLTeam
from nba.serializers import NBATeamsSerializer


class NHLTeamsView(ReadOnlyModelViewSet):
    queryset = NHLTeam.objects.all()
    serializer_class = NBATeamsSerializer
