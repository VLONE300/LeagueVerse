from django.urls import path
from rest_framework import routers

from nhl.views import NHLTeamsView

router = routers.SimpleRouter()
router.register(r'teams', NHLTeamsView)

urlpatterns = [
]

urlpatterns += router.urls
