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
