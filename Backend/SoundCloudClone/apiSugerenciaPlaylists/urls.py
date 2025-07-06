from django.urls import path
from .views import SugerenciaPlaylistsView

urlpatterns = [
    path('sugerencias/', SugerenciaPlaylistsView.as_view(), name='sugerencias-playlists'),
]
