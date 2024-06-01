from django.urls import path
from rest_framework import routers

from nba.views import NBATeamsView, NBAStandingsView, NBAScoreView, NBAScheduleView

router = routers.SimpleRouter()
router.register(r'teams', NBATeamsView)
router.register(r'standings', NBAStandingsView)
router.register(r'scores', NBAScoreView)
router.register(r'schedule', NBAScheduleView, basename='schedule')

urlpatterns = [

]

urlpatterns += router.urls
