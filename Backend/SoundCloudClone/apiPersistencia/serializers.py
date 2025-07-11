from rest_framework import serializers
from .models import Cancion, Playlist, Album, PlaylistCancion, Interaccion

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class CancionSerializer(serializers.ModelSerializer):
    album_titulo = serializers.CharField(source='album.titulo', read_only=True)
        
    class Meta:
        model = Cancion
        fields = '__all__'

class CancionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = ['titulo', 'descripcion', 'archivo_url', 'imagen_url', 'duracion', 'genero', 'album']

class PlaylistSerializer(serializers.ModelSerializer):
    total_canciones = serializers.SerializerMethodField()
    canciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = '__all__'
    
    def get_total_canciones(self, obj):
        return obj.canciones.count()
    
    def get_canciones(self, obj):
        playlist_canciones = PlaylistCancion.objects.filter(playlist=obj).order_by('orden')
        canciones = [pc.cancion for pc in playlist_canciones]
        return CancionSerializer(canciones, many=True).data

class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['titulo', 'descripcion', 'imagen_url', 'usuario_id','es_publica' ]

class PlaylistCancionSerializer(serializers.ModelSerializer):
    cancion_titulo = serializers.CharField(source='cancion.titulo', read_only=True)
    playlist_titulo = serializers.CharField(source='playlist.titulo', read_only=True)
    
    class Meta:
        model = PlaylistCancion
        fields = '__all__'

class PlaylistAgregarCancionSerializer(serializers.Serializer):
    """
    Serializer específico para agregar canciones a playlists
    """
    cancion_id = serializers.IntegerField(help_text="ID de la canción a agregar")
    orden = serializers.IntegerField(required=False, help_text="Posición en la playlist (opcional)")
    usuario_id = serializers.IntegerField(required=False, help_text="ID del usuario (solo para testing)")
    
    def validate_cancion_id(self, value):
        """Validar que la canción existe"""
        if not Cancion.objects.filter(pk=value).exists():
            raise serializers.ValidationError("La canción no existe")
        return value

class InteraccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaccion
        fields = '__all__'
