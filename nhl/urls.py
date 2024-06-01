from django.urls import path
from rest_framework import routers

from nhl.views import NHLTeamsView,NHLStandingsView

router = routers.SimpleRouter()
router.register(r'teams', NHLTeamsView)
router.register(r'standings', NHLStandingsView, basename='standings')

urlpatterns = [
]

urlpatterns += router.urls
