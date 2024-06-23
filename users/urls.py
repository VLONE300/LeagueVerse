from django.urls import path, include

from users.views import ActivateUser, AddFavoriteView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'}), name='activate'),
    path('favorites/', AddFavoriteView.as_view(), name='favorites'),
    path('favorites/<str:item_type>/<int:item_id>/', AddFavoriteView.as_view(), name='add_favorite'),
]

