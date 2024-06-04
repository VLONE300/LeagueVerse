from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from nba.models import NBAStanding, NBATeam, NBAGame
from nba.serializers import NBATeamsSerializer, NBAStandingsSerializer, NBAGamesSerializer


class NBATeamsView(ReadOnlyModelViewSet):
    queryset = NBATeam.objects.all()
    serializer_class = NBATeamsSerializer


class NBAStandingsView(ReadOnlyModelViewSet):
    serializer_class = NBAStandingsSerializer
    queryset = NBAStanding.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)

        data = {}
        for standing in queryset:
            conference = standing.team.conference
            if conference not in data:
                data[conference] = []
            serializer = self.get_serializer(standing)
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
