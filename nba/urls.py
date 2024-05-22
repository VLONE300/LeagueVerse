from django.urls import path
from rest_framework import routers

from nba.views import NBATeamsView, NBAStandingsView

router = routers.SimpleRouter()
router.register(r'teams', NBATeamsView)

urlpatterns = [
    path('standings/', NBAStandingsView.as_view(), name='nba_standings'),
]

urlpatterns += router.urls
