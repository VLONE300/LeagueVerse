from django.contrib.contenttypes.models import ContentType
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import League
from core.serializers import FavoriteSerializer
from nba.models import NBATeam
from nhl.models import NHLTeam
from users.models import Favorite


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        kwargs['data'] = {
            'uid': self.kwargs['uid'],
            'token': self.kwargs['token']
        }

        return serializer_class(*args, **kwargs)


class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_type, item_id):
        user = request.user
        model = None

        if item_type == 'nba':
            model = NBATeam
        elif item_type == 'nhl':
            model = NHLTeam
        elif item_type == 'league':
            model = League
        else:
            return Response({'detail': 'Invalid item type.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = model.objects.get(id=item_id)
        except model.DoesNotExist:
            return Response({'detail': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

        content_type = ContentType.objects.get_for_model(item)
        Favorite.objects.create(user=user, content_type=content_type, object_id=item.id)
        return Response({'detail': 'Item added to favorites.'}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
