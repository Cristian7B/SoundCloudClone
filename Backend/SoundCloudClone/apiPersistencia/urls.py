from django.urls import path
from .views import (
    CancionListCreateView, 
    CancionDetailView,
    PlaylistListCreateView, 
    PlaylistDetailView,
    AlbumListCreateView
)

urlpatterns = [
    # Endpoints de Canciones
    path('canciones/', CancionListCreateView.as_view(), name='cancion-list-create'),
    path('canciones/<int:pk>/', CancionDetailView.as_view(), name='cancion-detail'),
    
    # Endpoints de Playlists
    path('playlists/', PlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    
    # Endpoints de Albums
    path('albums/', AlbumListCreateView.as_view(), name='album-list-create'),
]
