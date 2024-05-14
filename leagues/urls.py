from rest_framework import routers

from leagues.views import LeagueView, NBATeamsView, NHLTeamsView

router = routers.SimpleRouter()
router.register(r'', LeagueView)
router.register(r'nba/teams', NBATeamsView)
router.register(r'nhl/teams', NHLTeamsView)

urlpatterns = []

urlpatterns += router.urls
