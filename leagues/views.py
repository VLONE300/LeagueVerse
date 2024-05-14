from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from leagues.models import League, NBATeams
from leagues.serializers import LeagueSerializer


class LeagueView(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
