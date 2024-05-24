from django.urls import path
from rest_framework import routers

from nba.views import NBATeamsView, NBAStandingsView, NBAGameView

router = routers.SimpleRouter()
router.register(r'teams', NBATeamsView)
router.register(r'scores', NBAGameView)

urlpatterns = [
    path('standings/', NBAStandingsView.as_view(), name='nba_standings'),
]

urlpatterns += router.urls
