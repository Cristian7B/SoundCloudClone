from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Cancion, Playlist, Album
from .serializers import CancionSerializer, PlaylistSerializer, AlbumSerializer, CancionCreateSerializer, PlaylistCreateSerializer

class CancionListCreateView(generics.ListCreateAPIView):
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
