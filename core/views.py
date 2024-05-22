from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import League
from core.serializers import LeagueSerializer


class LeagueView(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
