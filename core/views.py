from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import League
from core.serializers import LeagueSerializer


class LeagueView(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    lookup_field = 'name'


class StandingsView(ReadOnlyModelViewSet):
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


class GamesView(ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
