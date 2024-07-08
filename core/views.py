from django.http import JsonResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.models import League
from core.serializers import LeagueSerializer


class LeagueView(ReadOnlyModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    lookup_field = 'name'


class TeamView(ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {}
        for team in queryset:
            division = team.division
            if division not in data:
                data[division] = []
            serializer = self.get_serializer(team)
            data[division].append(serializer.data)
        return Response(data)


class StandingsView(ReadOnlyModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

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

    def list_schedule(self, model, serializer_class, request):
        today = timezone.now().date()

        unique_dates = model.objects.filter(status='Waiting', date__gte=today).values_list(
            'date', flat=True).distinct().order_by('date')[:3]

        date_games = []
        for date in unique_dates:
            games = model.objects.filter(status='Waiting', date=date).select_related('visitor_team').select_related(
                'home_team').order_by('date', 'time')

            date_games.append({
                'date': date,
                'games': games
            })

        serializer = serializer_class(date_games, many=True, context={'request': request})
        return Response(serializer.data)

    def list_game_dates(self, model):
        return Response([i.date for i in model.objects.all().order_by('-date')])


def health(request):
    return JsonResponse({'status': 'OK'})
