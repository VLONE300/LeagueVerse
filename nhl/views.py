from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from nhl.models import NHLTeam, NHLStanding, NHLGame
from nhl.serializers import NHLTeamsSerializer, NHLStandingsSerializer, NHLGamesSerializer


class NHLTeamsView(ReadOnlyModelViewSet):
    queryset = NHLTeam.objects.all()
    serializer_class = NHLTeamsSerializer


class NHLStandingsView(ReadOnlyModelViewSet):
    serializer_class = NHLStandingsSerializer
    queryset = NHLStanding.objects.all()

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


class NHLScoresView(ReadOnlyModelViewSet):
    queryset = NHLGame.objects.filter(status='Finished').order_by('-date')
    serializer_class = NHLGamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']


class NHLScheduleView(ReadOnlyModelViewSet):
    queryset = NHLGame.objects.filter(status='Waiting').order_by('-date')
    serializer_class = NHLGamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
