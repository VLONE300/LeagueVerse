from rest_framework import routers

from nhl.views import NHLTeamsView, NHLStandingsView, NHLScoreView, NHLScheduleView, NHLGamesDateView

router = routers.SimpleRouter()
router.register(r'teams', NHLTeamsView)
router.register(r'standings', NHLStandingsView, basename='standings')
router.register(r'scores', NHLScoreView, basename='scores')
router.register(r'schedule', NHLScheduleView, basename='schedule')
router.register(r'games-date', NHLGamesDateView, basename='games-date')

urlpatterns = [
]

urlpatterns += router.urls