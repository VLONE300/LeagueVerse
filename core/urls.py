from django.urls import path
from rest_framework import routers

from core.views import LeagueView

router = routers.SimpleRouter()
router.register(r'', LeagueView)

urlpatterns = [

]

urlpatterns += router.urls
