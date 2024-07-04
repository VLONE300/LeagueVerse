from rest_framework import routers

from nba.views import NBATeamsView, NBAStandingsView, NBAScoreView, NBAScheduleView, NBAGamesDateView, NBATeamStatsView

router = routers.SimpleRouter()
router.register(r'teams', NBATeamsView, basename='nba_teams')
router.register(r'standings', NBAStandingsView, basename='nba_standings')
router.register(r'scores', NBAScoreView, basename='nba_scores')
router.register(r'schedule', NBAScheduleView, basename='nba_schedule')
router.register(r'games-date', NBAGamesDateView, basename='nba_games-date')
router.register(r'stats', NBATeamStatsView, basename='nba_stats')

urlpatterns = [

]

urlpatterns += router.urls
