from rest_framework import routers

from nba.views import NBATeamsView, NBAStandingsView, NBAScoreView, NBAScheduleView, NBAGamesDateView, NBATeamStatsView

router = routers.SimpleRouter()
router.register(r'teams', NBATeamsView)
router.register(r'standings', NBAStandingsView)
router.register(r'scores', NBAScoreView)
router.register(r'schedule', NBAScheduleView, basename='schedule')
router.register(r'games-date', NBAGamesDateView, basename='games-date')
router.register(r'stats', NBATeamStatsView, basename='stats')

urlpatterns = [

]

urlpatterns += router.urls
