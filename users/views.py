from django.contrib.contenttypes.models import ContentType
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import League
from core.serializers import LeagueSerializer, FavoriteTeamSerializer
from nba.models import NBATeam
from nhl.models import NHLTeam
from users.models import FavoriteTeam


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        kwargs['data'] = {
            'uid': self.kwargs['uid'],
            'token': self.kwargs['token']
        }

        return serializer_class(*args, **kwargs)


class AddFavoriteLeagueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, league_id):
        user = request.user
        try:
            league = League.objects.get(id=league_id)
        except League.DoesNotExist:
            return Response({'detail': 'League not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.fav_league.add(league)
        user.save()
        return Response({'detail': 'League added to favorites.'}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        favorite_leagues = user.fav_league.all()
        serializer = LeagueSerializer(favorite_leagues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddFavoriteTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, team_type, team_id):
        user = request.user
        if team_type == 'nba':
            model = NBATeam
        elif team_type == 'nhl':
            model = NHLTeam
        else:
            return Response({'detail': 'Invalid team type.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = model.objects.get(id=team_id)
        except model.DoesNotExist:
            return Response({'detail': 'Team not found.'}, status=status.HTTP_404_NOT_FOUND)

        content_type = ContentType.objects.get_for_model(team)
        FavoriteTeam.objects.create(user=user, content_type=content_type, object_id=team.id)
        return Response({'detail': 'Team added to favorites.'}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        favorite_teams = FavoriteTeam.objects.filter(user=user)
        serializer = FavoriteTeamSerializer(favorite_teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
