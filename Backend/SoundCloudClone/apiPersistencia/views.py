"""
API views for music content persistence and management.

This module provides comprehensive API endpoints for managing the core music content
of the SoundCloud clone including songs, playlists, albums, and user interactions.
It handles CRUD operations, content relationships, and user-generated content management.

Classes:
    CancionListCreateView: List and create songs
    CancionDetailView: Retrieve, update, delete individual songs
    PlaylistListCreateView: List and create playlists
    PlaylistDetailView: Retrieve, update, delete individual playlists
    AlbumListCreateView: List and create albums
    AlbumDetailView: Retrieve, update, delete individual albums
    [... and many more specialized views for content management]

Features:
    - Complete CRUD operations for music content
    - User ownership validation and permissions
    - Playlist-song relationship management
    - User interaction tracking (likes, reposts, follows)
    - Content search and filtering capabilities
    - Statistics and analytics for user content

@author: Development Team
@version: 1.0
@since: 2024
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import Cancion, Playlist, Album, PlaylistCancion, Interaccion
from .serializers import (
    CancionSerializer, PlaylistSerializer, AlbumSerializer, 
    CancionCreateSerializer, PlaylistCreateSerializer, PlaylistCancionSerializer,
    PlaylistAgregarCancionSerializer, InteraccionSerializer, InteraccionCreateSerializer,
    InteraccionDetailSerializer
)


class CancionListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all songs and creating new songs.
    
    Provides endpoints for retrieving all available songs in the platform
    and for uploading new music content. Supports both authenticated and
    anonymous access with appropriate permission handling.
    
    Endpoints:
        GET /api/contenido/canciones/ - List all songs
        POST /api/contenido/canciones/ - Create new song
    
    Permissions:
        - AllowAny: Currently allows public access for development
        - TODO: Change to IsAuthenticated for production song uploads
    
    Create Process:
        - Validates song data using CancionCreateSerializer
        - Associates song with authenticated user or default test user
        - Returns success message with complete song details
    """
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer
    permission_classes = [AllowAny]  # Cambiar a [IsAuthenticated] cuando esté listo
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CancionCreateSerializer
        return CancionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # ID por defecto para testing
        
        cancion = serializer.save(usuario_id=usuario_id)
        
        return Response({
            'message': 'Canción creada exitosamente',
            'cancion': CancionSerializer(cancion).data
        }, status=status.HTTP_201_CREATED)

class CancionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer
    permission_classes = [AllowAny]

class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [AllowAny]  # Cambiar a [IsAuthenticated] cuando esté listo
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlaylistCreateSerializer
        return PlaylistSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # ID por defecto para testing
        
        playlist = serializer.save(usuario_id=usuario_id)
        
        return Response({
            'message': 'Playlist creada exitosamente',
            'playlist': PlaylistSerializer(playlist).data
        }, status=status.HTTP_201_CREATED)

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [AllowAny]

class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # ID por defecto para testing
        
        album = serializer.save(usuario_id=usuario_id)
        
        return Response({
            'message': 'Album creado exitosamente',
            'album': AlbumSerializer(album).data
        }, status=status.HTTP_201_CREATED)

class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]

class AlbumCancionesView(generics.ListAPIView):
    """
    Endpoint para obtener todas las canciones de un álbum específico
    URL: /albums/{album_id}/canciones/
    """
    serializer_class = CancionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        album_id = self.kwargs['pk']
        return Cancion.objects.filter(album_id=album_id).order_by('created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        album_id = self.kwargs['pk']
        
        try:
            album = Album.objects.get(pk=album_id)
        except Album.DoesNotExist:
            return Response({
                'error': 'Álbum no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'album': {
                'id': album.album_id,
                'titulo': album.titulo,
                'descripcion': album.descripcion,
                'imagen_url': album.imagen_url
            },
            'total_canciones': queryset.count(),
            'canciones': serializer.data
        })

class PlaylistCancionesView(generics.ListAPIView):
    """
    Endpoint para obtener todas las canciones de una playlist específica
    URL: /playlists/{playlist_id}/canciones/
    """
    serializer_class = CancionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        playlist_id = self.kwargs['pk']
        # Obtener canciones ordenadas según el orden en la playlist
        playlist_canciones = PlaylistCancion.objects.filter(
            playlist_id=playlist_id
        ).order_by('orden', 'added_at')
        
        return [pc.cancion for pc in playlist_canciones]
    
    def list(self, request, *args, **kwargs):
        playlist_id = self.kwargs['pk']
        
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not playlist.es_publica:
            if not request.user.is_authenticated or request.user.user_id != playlist.usuario_id:
                return Response({
                    'error': 'No tienes permisos para ver esta playlist privada'
                }, status=status.HTTP_403_FORBIDDEN)
        
        canciones = self.get_queryset()
        serializer = self.get_serializer(canciones, many=True)
        
        return Response({
            'playlist': {
                'id': playlist.playlist_id,
                'titulo': playlist.titulo,
                'descripcion': playlist.descripcion,
                'imagen_url': playlist.imagen_url,
                'es_publica': playlist.es_publica
            },
            'total_canciones': len(canciones),
            'canciones': serializer.data
        })

class CancionBusquedaView(generics.ListAPIView):
    """
    Endpoint para búsqueda en tiempo real de canciones
    URL: /canciones/buscar/?q={termino_busqueda}
    """
    serializer_class = CancionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        
        if not query:
            return Cancion.objects.none()
        
        return Cancion.objects.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(genero__icontains=query)
        ).order_by('-reproducciones', '-created_at')
    
    def list(self, request, *args, **kwargs):
        query = self.request.query_params.get('q', '')
        
        if not query:
            return Response({
                'message': 'Parámetro de búsqueda "q" es requerido',
                'ejemplo': '/canciones/buscar/?q=rock'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(query) < 2:
            return Response({
                'message': 'El término de búsqueda debe tener al menos 2 caracteres'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'termino_busqueda': query,
            'total_resultados': queryset.count(),
            'resultados': serializer.data
        })

class PlaylistAgregarCancionView(generics.CreateAPIView):
    """
    Endpoint para agregar una canción a una playlist
    URL: /playlists/{playlist_id}/agregar-cancion/
    """
    serializer_class = PlaylistAgregarCancionSerializer
    permission_classes = [AllowAny]  # Cambiar a [IsAuthenticated] cuando esté listo
    
    def create(self, request, *args, **kwargs):
        playlist_id = self.kwargs['pk']
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cancion_id = serializer.validated_data['cancion_id']
        orden = serializer.validated_data.get('orden')
        
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        cancion = Cancion.objects.get(pk=cancion_id)
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = serializer.validated_data.get('usuario_id', 1)  # Para testing
        
        if playlist.usuario_id != usuario_id:
            return Response({
                'error': 'No tienes permisos para modificar esta playlist'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if PlaylistCancion.objects.filter(playlist=playlist, cancion=cancion).exists():
            return Response({
                'error': 'La canción ya está en la playlist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if orden is None:
            ultimo_orden = PlaylistCancion.objects.filter(playlist=playlist).count()
            orden = ultimo_orden
        
        playlist_cancion = PlaylistCancion.objects.create(
            playlist=playlist,
            cancion=cancion,
            orden=orden
        )
        
        response_serializer = PlaylistCancionSerializer(playlist_cancion)
        
        return Response({
            'message': 'Canción agregada a la playlist exitosamente',
            'playlist_cancion': response_serializer.data
        }, status=status.HTTP_201_CREATED)

class PlaylistEliminarCancionView(generics.DestroyAPIView):
    """
    Endpoint para eliminar una canción de una playlist
    URL: /playlists/{playlist_id}/canciones/{cancion_id}/eliminar/
    """
    permission_classes = [AllowAny]  # Cambiar a [IsAuthenticated] cuando esté listo
    
    def destroy(self, request, *args, **kwargs):
        playlist_id = self.kwargs['playlist_pk']
        cancion_id = self.kwargs['cancion_pk']
        
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # Para testing
        
        if playlist.usuario_id != usuario_id:
            return Response({
                'error': 'No tienes permisos para modificar esta playlist'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            playlist_cancion = PlaylistCancion.objects.get(
                playlist_id=playlist_id, 
                cancion_id=cancion_id
            )
            playlist_cancion.delete()
            
            return Response({
                'message': 'Canción eliminada de la playlist exitosamente'
            }, status=status.HTTP_200_OK)
            
        except PlaylistCancion.DoesNotExist:
            return Response({
                'error': 'La canción no está en la playlist'
            }, status=status.HTTP_404_NOT_FOUND)

class PlaylistReordenarCancionesView(generics.UpdateAPIView):
    """
    Endpoint para reordenar canciones en una playlist
    URL: /playlists/{playlist_id}/reordenar/
    Body: {"canciones_orden": [{"cancion_id": 1, "orden": 0}, {"cancion_id": 3, "orden": 1}]}
    """
    permission_classes = [AllowAny]  # Cambiar a [IsAuthenticated] cuando esté listo
    
    def update(self, request, *args, **kwargs):
        playlist_id = self.kwargs['pk']
        canciones_orden = request.data.get('canciones_orden', [])
        
        if not canciones_orden:
            return Response({
                'error': 'canciones_orden es requerido',
                'formato': [{"cancion_id": 1, "orden": 0}, {"cancion_id": 3, "orden": 1}]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # Para testing
        
        if playlist.usuario_id != usuario_id:
            return Response({
                'error': 'No tienes permisos para modificar esta playlist'
            }, status=status.HTTP_403_FORBIDDEN)
        
        actualizadas = 0
        errores = []
        
        for item in canciones_orden:
            cancion_id = item.get('cancion_id')
            nuevo_orden = item.get('orden')
            
            if cancion_id is None or nuevo_orden is None:
                errores.append(f'cancion_id y orden son requeridos para cada item')
                continue
            
            try:
                playlist_cancion = PlaylistCancion.objects.get(
                    playlist_id=playlist_id,
                    cancion_id=cancion_id
                )
                playlist_cancion.orden = nuevo_orden
                playlist_cancion.save()
                actualizadas += 1
                
            except PlaylistCancion.DoesNotExist:
                errores.append(f'Canción {cancion_id} no está en la playlist')
        
        response_data = {
            'message': f'{actualizadas} canciones reordenadas exitosamente',
            'canciones_actualizadas': actualizadas
        }
        
        if errores:
            response_data['errores'] = errores
        
        return Response(response_data, status=status.HTTP_200_OK)

class PlaylistCancionListView(generics.ListAPIView):
    """
    Endpoint para listar todas las relaciones playlist-cancion
    URL: /playlist-canciones/
    """
    queryset = PlaylistCancion.objects.all().order_by('-added_at')
    serializer_class = PlaylistCancionSerializer
    permission_classes = [AllowAny]

class UsuarioPlaylistsView(generics.ListAPIView):
    """
    Endpoint para obtener todas las playlists de un usuario específico
    URL: /usuarios/{usuario_id}/playlists/
    """
    serializer_class = PlaylistSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        usuario_id = self.kwargs['usuario_id']
        return Playlist.objects.filter(usuario_id=usuario_id).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        usuario_id = self.kwargs['usuario_id']
        queryset = self.get_queryset()
        
        mostrar_privadas = False
        if request.user.is_authenticated and request.user.user_id == usuario_id:
            mostrar_privadas = True
        if not mostrar_privadas:
            queryset = queryset.filter(es_publica=True)
        
        serializer = self.get_serializer(queryset, many=True)
        
        playlists_publicas = []
        playlists_privadas = []
        
        for playlist_data in serializer.data:
            if playlist_data['es_publica']:
                playlists_publicas.append(playlist_data)
            else:
                playlists_privadas.append(playlist_data)
        
        response_data = {
            'usuario_id': usuario_id,
            'total_playlists': queryset.count(),
            'playlists_publicas': {
                'total': len(playlists_publicas),
                'playlists': playlists_publicas
            }
        }
        
        if mostrar_privadas and playlists_privadas:
            response_data['playlists_privadas'] = {
                'total': len(playlists_privadas),
                'playlists': playlists_privadas
            }
        
        return Response(response_data, status=status.HTTP_200_OK)

class UsuarioCancionesView(generics.ListAPIView):
    """
    Endpoint para obtener todas las canciones de un usuario específico
    URL: /usuarios/{usuario_id}/canciones/
    """
    serializer_class = CancionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        usuario_id = self.kwargs['usuario_id']
        return Cancion.objects.filter(usuario_id=usuario_id).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        usuario_id = self.kwargs['usuario_id']
        queryset = self.get_queryset()
        
        total_reproducciones = sum(cancion.reproducciones for cancion in queryset)
        total_likes = sum(cancion.likes_count for cancion in queryset)
        total_reposts = sum(cancion.reposts_count for cancion in queryset)
        
        generos = list(set(cancion.genero for cancion in queryset if cancion.genero))
        
        albums_ids = list(set(cancion.album_id for cancion in queryset if cancion.album_id))
        albums = Album.objects.filter(album_id__in=albums_ids) if albums_ids else []
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'usuario_id': usuario_id,
            'total_canciones': queryset.count(),
            'estadisticas': {
                'total_reproducciones': total_reproducciones,
                'total_likes': total_likes,
                'total_reposts': total_reposts,
                'generos_musicales': generos,
                'total_albums': len(albums)
            },
            'canciones': serializer.data
        }, status=status.HTTP_200_OK)

class InteraccionCreateView(generics.CreateAPIView):
    """
    Endpoint para crear interacciones (like, repost, follow)
    URL: /interacciones/
    """
    serializer_class = InteraccionCreateSerializer
    permission_classes = [AllowAny]  # Cambiar a [IsAuthenticated] cuando esté listo
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tipo = serializer.validated_data['tipo']
        cancion_id = serializer.validated_data.get('cancion_id')
        playlist_id = serializer.validated_data.get('playlist_id')
        usuario_objetivo_id = serializer.validated_data.get('usuario_objetivo_id')
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = serializer.validated_data.get('usuario_id', 1)  # Para testing
        
        if tipo == 'follow' and usuario_id == usuario_objetivo_id:
            return Response({
                'error': 'No puedes seguirte a ti mismo'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        filtros = {'usuario_id': usuario_id, 'tipo': tipo}
        
        if cancion_id:
            filtros['cancion_id'] = cancion_id
        elif playlist_id:
            filtros['playlist_id'] = playlist_id
        elif usuario_objetivo_id:
            filtros['usuario_objetivo_id'] = usuario_objetivo_id
        
        if Interaccion.objects.filter(**filtros).exists():
            return Response({
                'error': f'Ya has hecho {tipo} a este elemento'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        interaccion_data = {
            'usuario_id': usuario_id,
            'tipo': tipo
        }
        
        if cancion_id:
            interaccion_data['cancion_id'] = cancion_id
        elif playlist_id:
            interaccion_data['playlist_id'] = playlist_id
        elif usuario_objetivo_id:
            interaccion_data['usuario_objetivo_id'] = usuario_objetivo_id
        
        interaccion = Interaccion.objects.create(**interaccion_data)
        
        if tipo == 'like' and cancion_id:
            cancion = Cancion.objects.get(pk=cancion_id)
            cancion.likes_count += 1
            cancion.save()
        elif tipo == 'repost' and cancion_id:
            cancion = Cancion.objects.get(pk=cancion_id)
            cancion.reposts_count += 1
            cancion.save()
        
        response_serializer = InteraccionDetailSerializer(interaccion)
        
        return Response({
            'message': f'{tipo.capitalize()} registrado exitosamente',
            'interaccion': response_serializer.data
        }, status=status.HTTP_201_CREATED)

class InteraccionDeleteView(generics.DestroyAPIView):
    """
    Endpoint para eliminar interacciones (unlike, unrepost, unfollow)
    URL: /interacciones/{interaccion_id}/
    """
    queryset = Interaccion.objects.all()
    permission_classes = [AllowAny]  # Cambiar a [IsAuthenticated] cuando esté listo
    
    def destroy(self, request, *args, **kwargs):
        interaccion = self.get_object()
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # Para testing
        
        if interaccion.usuario_id != usuario_id:
            return Response({
                'error': 'No tienes permisos para eliminar esta interacción'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if interaccion.tipo == 'like' and interaccion.cancion:
            cancion = interaccion.cancion
            cancion.likes_count = max(0, cancion.likes_count - 1)
            cancion.save()
        elif interaccion.tipo == 'repost' and interaccion.cancion:
            cancion = interaccion.cancion
            cancion.reposts_count = max(0, cancion.reposts_count - 1)
            cancion.save()
        
        tipo = interaccion.tipo
        interaccion.delete()
        
        return Response({
            'message': f'{tipo.capitalize()} eliminado exitosamente'
        }, status=status.HTTP_200_OK)

class UsuarioInteraccionesView(generics.ListAPIView):
    """
    Endpoint para obtener todas las interacciones de un usuario
    URL: /usuarios/{usuario_id}/interacciones/
    """
    serializer_class = InteraccionDetailSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        usuario_id = self.kwargs['usuario_id']
        tipo = self.request.query_params.get('tipo')  # Filtro opcional por tipo
        
        queryset = Interaccion.objects.filter(usuario_id=usuario_id)
        
        if tipo and tipo in ['like', 'repost', 'follow']:
            queryset = queryset.filter(tipo=tipo)
        
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        usuario_id = self.kwargs['usuario_id']
        queryset = self.get_queryset()
        
        likes = queryset.filter(tipo='like')
        reposts = queryset.filter(tipo='repost')
        follows = queryset.filter(tipo='follow')
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'usuario_id': usuario_id,
            'total_interacciones': queryset.count(),
            'estadisticas': {
                'total_likes': likes.count(),
                'total_reposts': reposts.count(),
                'total_follows': follows.count()
            },
            'interacciones': serializer.data
        }, status=status.HTTP_200_OK)

class InteraccionToggleView(generics.GenericAPIView):
    """
    Endpoint para hacer toggle de interacciones (crear si no existe, eliminar si existe)
    URL: /interacciones/toggle/
    """
    serializer_class = InteraccionCreateSerializer
    permission_classes = [AllowAny]  
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tipo = serializer.validated_data['tipo']
        cancion_id = serializer.validated_data.get('cancion_id')
        playlist_id = serializer.validated_data.get('playlist_id')
        usuario_objetivo_id = serializer.validated_data.get('usuario_objetivo_id')
        
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = serializer.validated_data.get('usuario_id', 1)  # Para testing
        
        filtros = {'usuario_id': usuario_id, 'tipo': tipo}
        
        if cancion_id:
            filtros['cancion_id'] = cancion_id
        elif playlist_id:
            filtros['playlist_id'] = playlist_id
        elif usuario_objetivo_id:
            filtros['usuario_objetivo_id'] = usuario_objetivo_id
        
        try:
            interaccion = Interaccion.objects.get(**filtros)
            
            # Ya existe, eliminarla
            if interaccion.tipo == 'like' and interaccion.cancion:
                cancion = interaccion.cancion
                cancion.likes_count = max(0, cancion.likes_count - 1)
                cancion.save()
            elif interaccion.tipo == 'repost' and interaccion.cancion:
                cancion = interaccion.cancion
                cancion.reposts_count = max(0, cancion.reposts_count - 1)
                cancion.save()
            
            interaccion.delete()
            
            return Response({
                'message': f'{tipo.capitalize()} eliminado',
                'accion': 'eliminado',
                'activo': False
            }, status=status.HTTP_200_OK)
            
        except Interaccion.DoesNotExist:
            interaccion_data = {
                'usuario_id': usuario_id,
                'tipo': tipo
            }
            
            if cancion_id:
                interaccion_data['cancion_id'] = cancion_id
            elif playlist_id:
                interaccion_data['playlist_id'] = playlist_id
            elif usuario_objetivo_id:
                interaccion_data['usuario_objetivo_id'] = usuario_objetivo_id
            
            interaccion = Interaccion.objects.create(**interaccion_data)
            
            if tipo == 'like' and cancion_id:
                cancion = Cancion.objects.get(pk=cancion_id)
                cancion.likes_count += 1
                cancion.save()
            elif tipo == 'repost' and cancion_id:
                cancion = Cancion.objects.get(pk=cancion_id)
                cancion.reposts_count += 1
                cancion.save()
            
            response_serializer = InteraccionDetailSerializer(interaccion)
            
            return Response({
                'message': f'{tipo.capitalize()} agregado',
                'accion': 'creado',
                'activo': True,
                'interaccion': response_serializer.data
            }, status=status.HTTP_201_CREATED)