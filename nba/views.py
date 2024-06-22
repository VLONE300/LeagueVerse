from rest_framework.viewsets import ReadOnlyModelViewSet
from core.views import StandingsView, GamesView
from nba.models import NBAStanding, NBATeam, NBAGame
from nba.serializers import NBATeamsSerializer, NBAStandingsSerializer, NBAScheduleSerializer, \
    NBAGamesDateSerializer, NBAGameDetailSerializer, NBAGameListSerializer


class NBATeamsView(ReadOnlyModelViewSet):
    queryset = NBATeam.objects.all()
    serializer_class = NBATeamsSerializer


class NBAStandingsView(StandingsView):
    serializer_class = NBAStandingsSerializer
    queryset = NBAStanding.objects.all()


class NBAScoreView(GamesView):
    queryset = NBAGame.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NBAGameDetailSerializer
        return NBAGameListSerializer


class NBAScheduleView(GamesView):
    queryset = NBAGame.objects.all()
    serializer_class = NBAScheduleSerializer


class NBAGamesDateView(ReadOnlyModelViewSet):
    queryset = NBAGame.objects.all()
    serializer_class = NBAGamesDateSerializer

#  slug = date_str+game.home_team.name.upper()[:3]
