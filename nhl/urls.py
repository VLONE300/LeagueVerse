from django.urls import path
from rest_framework import routers

from nhl.views import NHLTeamsView, NHLStandingsView, NHLScoresView, NHLScheduleView

router = routers.SimpleRouter()
router.register(r'teams', NHLTeamsView)
router.register(r'standings', NHLStandingsView, basename='standings')
router.register(r'scores', NHLScoresView, basename='scores')
router.register(r'schedule', NHLScheduleView, basename='schedule')

urlpatterns = [
]

urlpatterns += router.urls