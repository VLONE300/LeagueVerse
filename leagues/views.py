from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from leagues.models import League, NBATeams, NHLTeams, NBAStandings
from leagues.serializers import LeagueSerializer, TeamsSerializer, NBATeamsSerializer, NHLTeamsSerializer, \
    NBAStandingsSerializer


class LeagueView(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer


class TeamsView(ReadOnlyModelViewSet):
    serializer_class = TeamsSerializer


class NBATeamsView(TeamsView):
    queryset = NBATeams.objects.all()
    serializer_class = NBATeamsSerializer


class NHLTeamsView(TeamsView):
    queryset = NHLTeams.objects.all()
    serializer_class = NHLTeamsSerializer


class NBAStandingsView(APIView):
    serializer_class = NBAStandingsSerializer

    def get_queryset(self):
        queryset = NBAStandings.objects.all()
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        data = {}

        for standing in queryset:
            conference = standing.team.conference
            if conference not in data:
                data[conference] = []
            serializer = NBAStandingsSerializer(standing)
            data[conference].append(serializer.data)

        return Response(data)
