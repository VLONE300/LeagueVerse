from django.urls import path, include

from users.views import ActivateUser, AddFavoriteLeagueView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'}), name='activate'),
    path('add-favorite-league/<int:league_id>/', AddFavoriteLeagueView.as_view(), name='add_favorite_league'),
    path('favorite-leagues/', AddFavoriteLeagueView.as_view(), name='favorite_leagues'),
]
