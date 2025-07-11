from django.urls import path
from .views import (
    CancionListCreateView, 
    CancionDetailView,
    PlaylistListCreateView, 
    PlaylistDetailView,
    AlbumListCreateView,
    AlbumDetailView,
    AlbumCancionesView,
    PlaylistCancionesView,
    CancionBusquedaView,
    PlaylistAgregarCancionView,
    PlaylistEliminarCancionView,
    PlaylistReordenarCancionesView,
    PlaylistCancionListView,
    UsuarioPlaylistsView,
    UsuarioCancionesView,
    InteraccionCreateView,
    InteraccionDeleteView,
    UsuarioInteraccionesView,
    InteraccionToggleView
)

urlpatterns = [
    # Endpoints de Canciones
    path('canciones/', CancionListCreateView.as_view(), name='cancion-list-create'),
    path('canciones/<int:pk>/', CancionDetailView.as_view(), name='cancion-detail'),
    path('canciones/buscar/', CancionBusquedaView.as_view(), name='cancion-busqueda'),
    
    # Endpoints de Playlists
    path('playlists/', PlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/<int:pk>/canciones/', PlaylistCancionesView.as_view(), name='playlist-canciones'),
    path('playlists/<int:pk>/agregar-cancion/', PlaylistAgregarCancionView.as_view(), name='playlist-agregar-cancion'),
    path('playlists/<int:playlist_pk>/canciones/<int:cancion_pk>/eliminar/', PlaylistEliminarCancionView.as_view(), name='playlist-eliminar-cancion'),
    path('playlists/<int:pk>/reordenar/', PlaylistReordenarCancionesView.as_view(), name='playlist-reordenar'),
    
    # Endpoints de Albums
    path('albums/', AlbumListCreateView.as_view(), name='album-list-create'),
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('albums/<int:pk>/canciones/', AlbumCancionesView.as_view(), name='album-canciones'),
    
    # Endpoints de Relaciones Playlist-Cancion
    path('playlist-canciones/', PlaylistCancionListView.as_view(), name='playlist-cancion-list'),
    
    # Endpoints de Usuario
    path('usuarios/<int:usuario_id>/playlists/', UsuarioPlaylistsView.as_view(), name='usuario-playlists'),
    path('usuarios/<int:usuario_id>/canciones/', UsuarioCancionesView.as_view(), name='usuario-canciones'),
    path('usuarios/<int:usuario_id>/interacciones/', UsuarioInteraccionesView.as_view(), name='usuario-interacciones'),
    
    # Endpoints de Interacciones
    path('interacciones/', InteraccionCreateView.as_view(), name='interaccion-create'),
    path('interacciones/<int:pk>/', InteraccionDeleteView.as_view(), name='interaccion-delete'),
    path('interacciones/toggle/', InteraccionToggleView.as_view(), name='interaccion-toggle'),
]
