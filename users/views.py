from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import League
from core.serializers import LeagueSerializer


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
