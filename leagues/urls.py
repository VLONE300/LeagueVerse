from django.urls import path
from rest_framework import routers

from leagues.views import LeagueView, NBATeamsView, NHLTeamsView, NBAStandingsView

router = routers.SimpleRouter()
router.register(r'', LeagueView)
router.register(r'nba/teams', NBATeamsView)
# router.register(r'nba/standings', NBAStandingsView, basename='nba-standings')
router.register(r'nhl/teams', NHLTeamsView)

urlpatterns = [
    path('nba/standings/', NBAStandingsView.as_view(), name='nba-standings'),
]

urlpatterns += router.urls
