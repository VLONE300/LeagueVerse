from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers

from core.views import LeagueView, health

router = routers.SimpleRouter()
router.register(r'', LeagueView)

urlpatterns = [
    path('health/', health, name='health'),
]

urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
