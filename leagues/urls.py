from rest_framework import routers

from leagues.views import LeagueView

router = routers.SimpleRouter()
router.register(r'', LeagueView)

urlpatterns = []

urlpatterns += router.urls
