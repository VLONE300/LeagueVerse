from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from nba.models import NBAStanding, NBATeam
from nba.serializers import NBATeamsSerializer, NBAStandingsSerializer


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
