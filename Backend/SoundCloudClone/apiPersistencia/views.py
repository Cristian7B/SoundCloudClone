from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import Cancion, Playlist, Album, PlaylistCancion
from .serializers import (
    CancionSerializer, PlaylistSerializer, AlbumSerializer, 
    CancionCreateSerializer, PlaylistCreateSerializer, PlaylistCancionSerializer,
    PlaylistAgregarCancionSerializer
)

class CancionListCreateView(generics.ListCreateAPIView):
    """
        Vista para listar todas las canciones y crear nuevas.

        Endpoints:
            GET /canciones/ - Lista todas las canciones
            POST /canciones/ - Crea una nueva canción

        Permisos: Acceso público (temporalmente)
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
    """
        Vista para gestionar una canción específica.

        Endpoints:
            GET /canciones/{id}/ - Obtiene detalles de una canción
            PUT /canciones/{id}/ - Actualiza una canción
            DELETE /canciones/{id}/ - Elimina una canción
    """
    queryset = Cancion.objects.all()
    serializer_class = CancionSerializer
    permission_classes = [AllowAny]

class PlaylistListCreateView(generics.ListCreateAPIView):
    """
        Vista para listar todas las playlists y crear nuevas.

        Endpoints:
            GET /playlists/ - Lista todas las playlists
            POST /playlists/ - Crea una nueva playlist

        Notas:
            - Al crear, asigna automáticamente el usuario_id del creador
            - Soporta creación con usuario autenticado o ID de prueba
    """
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
    """
        Vista para gestionar una playlist específica.

        Endpoints:
            GET /playlists/{id}/ - Obtiene detalles de una playlist
            PUT /playlists/{id}/ - Actualiza una playlist
            DELETE /playlists/{id}/ - Elimina una playlist
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [AllowAny]

class AlbumListCreateView(generics.ListCreateAPIView):
    """
        Vista para listar todos los álbumes y crear nuevos.

        Endpoints:
            GET /albums/ - Lista todos los álbumes
            POST /albums/ - Crea un nuevo álbum

        Notas:
            - Asigna automáticamente el usuario_id del creador
    """
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
    """
        Vista para gestionar un álbum específico.

        Endpoints:
            GET /albums/{id}/ - Obtiene detalles de un álbum
            PUT /albums/{id}/ - Actualiza un álbum
            DELETE /albums/{id}/ - Elimina un álbum
    """
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
        
        # Verificar que el álbum existe
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
        
        # Verificar que la playlist existe
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar si la playlist es pública o si el usuario tiene acceso
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
        
        # Búsqueda en título, descripción y género
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
        
        # Validar datos con el serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cancion_id = serializer.validated_data['cancion_id']
        orden = serializer.validated_data.get('orden')
        
        # Verificar que la playlist existe
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener canción (ya validada por el serializer)
        cancion = Cancion.objects.get(pk=cancion_id)
        
        # Verificar permisos (solo el creador puede modificar la playlist)
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = serializer.validated_data.get('usuario_id', 1)  # Para testing
        
        if playlist.usuario_id != usuario_id:
            return Response({
                'error': 'No tienes permisos para modificar esta playlist'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Verificar si la canción ya está en la playlist
        if PlaylistCancion.objects.filter(playlist=playlist, cancion=cancion).exists():
            return Response({
                'error': 'La canción ya está en la playlist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcular el orden (último + 1 si no se especifica)
        if orden is None:
            ultimo_orden = PlaylistCancion.objects.filter(playlist=playlist).count()
            orden = ultimo_orden
        
        # Crear la relación
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
        
        # Verificar que la playlist existe
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar permisos
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # Para testing
        
        if playlist.usuario_id != usuario_id:
            return Response({
                'error': 'No tienes permisos para modificar esta playlist'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Buscar y eliminar la relación
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
        
        # Verificar que la playlist existe
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response({
                'error': 'Playlist no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar permisos
        if request.user.is_authenticated:
            usuario_id = request.user.user_id
        else:
            usuario_id = request.data.get('usuario_id', 1)  # Para testing
        
        if playlist.usuario_id != usuario_id:
            return Response({
                'error': 'No tienes permisos para modificar esta playlist'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Actualizar el orden de las canciones
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
