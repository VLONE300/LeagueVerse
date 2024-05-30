from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from nba.models import NBAStanding, NBATeam, NBAGame
from nba.serializers import NBATeamsSerializer, NBAStandingsSerializer, NBAGamesSerializer


class NBATeamsView(ReadOnlyModelViewSet):
    queryset = NBATeam.objects.all()
    serializer_class = NBATeamsSerializer


class NBAStandingsView(APIView):
    serializer_class = NBAStandingsSerializer

    def get_queryset(self):
        queryset = NBAStanding.objects.all()
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


class NBAScoreView(ReadOnlyModelViewSet):
    queryset = NBAGame.objects.filter(status='Finished').order_by('-date')
    serializer_class = NBAGamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']


class NBAScheduleView(ReadOnlyModelViewSet):
    queryset = NBAGame.objects.filter(status='Waiting').order_by('-date')
    serializer_class = NBAGamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
