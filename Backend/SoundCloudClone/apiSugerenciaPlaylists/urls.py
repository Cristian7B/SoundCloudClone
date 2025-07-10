from django.urls import path
from .views import SugerenciaPlaylistsView

urlpatterns = [
    path('', SugerenciaPlaylistsView.as_view(), name='sugerencias-playlists'),
]
