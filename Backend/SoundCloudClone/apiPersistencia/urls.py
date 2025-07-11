"""
URL configuration for music content persistence API.

This module defines all URL patterns for the content management API endpoints,
organizing routes for songs, playlists, albums, and user interactions in a
RESTful structure with clear resource hierarchies.

URL Groups:
    Songs (canciones/):
        - CRUD operations for individual songs
        - Search functionality for content discovery
    
    Playlists (playlists/):
        - CRUD operations for playlists
        - Song management within playlists (add, remove, reorder)
        - Playlist content retrieval
    
    Albums (albums/):
        - CRUD operations for albums
        - Album track listing and management
    
    User Content (usuarios/{id}/):
        - User-specific content retrieval
        - Personal playlists and songs
        - User interaction history
    
    Interactions (interacciones/):
        - User engagement tracking (likes, reposts, follows)
        - Social interaction management

API Design:
    - RESTful conventions with clear resource naming
    - Hierarchical URL structure for related resources
    - Consistent parameter naming across endpoints
    - Support for both individual and bulk operations

@author: Development Team
@version: 1.0
@since: 2024
"""

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
    # Song Management Endpoints
    # GET /api/contenido/canciones/ - List all songs
    # POST /api/contenido/canciones/ - Create new song
    path('canciones/', CancionListCreateView.as_view(), name='cancion-list-create'),
    
    # GET /api/contenido/canciones/{id}/ - Retrieve specific song
    # PUT /api/contenido/canciones/{id}/ - Update song
    # DELETE /api/contenido/canciones/{id}/ - Delete song
    path('canciones/<int:pk>/', CancionDetailView.as_view(), name='cancion-detail'),
    
    # GET /api/contenido/canciones/buscar/?q=query - Search songs
    path('canciones/buscar/', CancionBusquedaView.as_view(), name='cancion-busqueda'),
    
    # Playlist Management Endpoints
    # GET /api/contenido/playlists/ - List all playlists
    # POST /api/contenido/playlists/ - Create new playlist
    path('playlists/', PlaylistListCreateView.as_view(), name='playlist-list-create'),
    
    # GET /api/contenido/playlists/{id}/ - Retrieve specific playlist
    # PUT /api/contenido/playlists/{id}/ - Update playlist
    # DELETE /api/contenido/playlists/{id}/ - Delete playlist
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    
    # GET /api/contenido/playlists/{id}/canciones/ - List playlist songs
    path('playlists/<int:pk>/canciones/', PlaylistCancionesView.as_view(), name='playlist-canciones'),
    
    # POST /api/contenido/playlists/{id}/agregar-cancion/ - Add song to playlist
    path('playlists/<int:pk>/agregar-cancion/', PlaylistAgregarCancionView.as_view(), name='playlist-agregar-cancion'),
    
    # DELETE /api/contenido/playlists/{playlist_id}/canciones/{song_id}/eliminar/ - Remove song from playlist
    path('playlists/<int:playlist_pk>/canciones/<int:cancion_pk>/eliminar/', PlaylistEliminarCancionView.as_view(), name='playlist-eliminar-cancion'),
    
    # PUT /api/contenido/playlists/{id}/reordenar/ - Reorder playlist songs
    path('playlists/<int:pk>/reordenar/', PlaylistReordenarCancionesView.as_view(), name='playlist-reordenar'),
    
    # Album Management Endpoints
    # GET /api/contenido/albums/ - List all albums
    # POST /api/contenido/albums/ - Create new album
    path('albums/', AlbumListCreateView.as_view(), name='album-list-create'),
    
    # GET /api/contenido/albums/{id}/ - Retrieve specific album
    # PUT /api/contenido/albums/{id}/ - Update album
    # DELETE /api/contenido/albums/{id}/ - Delete album
    path('albums/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    
    # GET /api/contenido/albums/{id}/canciones/ - List album tracks
    path('albums/<int:pk>/canciones/', AlbumCancionesView.as_view(), name='album-canciones'),
    
    # Playlist-Song Relationship Management
    # GET /api/contenido/playlist-canciones/ - List all playlist-song relationships
    path('playlist-canciones/', PlaylistCancionListView.as_view(), name='playlist-cancion-list'),
    
    # User Content Endpoints
    # GET /api/contenido/usuarios/{user_id}/playlists/ - List user's playlists
    path('usuarios/<int:usuario_id>/playlists/', UsuarioPlaylistsView.as_view(), name='usuario-playlists'),
    
    # GET /api/contenido/usuarios/{user_id}/canciones/ - List user's songs
    path('usuarios/<int:usuario_id>/canciones/', UsuarioCancionesView.as_view(), name='usuario-canciones'),
    
    # GET /api/contenido/usuarios/{user_id}/interacciones/ - List user's interactions
    path('usuarios/<int:usuario_id>/interacciones/', UsuarioInteraccionesView.as_view(), name='usuario-interacciones'),
    
    # User Interaction Endpoints
    # POST /api/contenido/interacciones/ - Create new interaction (like, repost, follow)
    path('interacciones/', InteraccionCreateView.as_view(), name='interaccion-create'),
    
    # DELETE /api/contenido/interacciones/{id}/ - Remove interaction
    path('interacciones/<int:pk>/', InteraccionDeleteView.as_view(), name='interaccion-delete'),
    
    # POST /api/contenido/interacciones/toggle/ - Toggle interaction (like/unlike, follow/unfollow)
    path('interacciones/toggle/', InteraccionToggleView.as_view(), name='interaccion-toggle'),
]
