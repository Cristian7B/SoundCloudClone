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
        fields = ['titulo', 'descripcion', 'imagen_url', 'es_publica']

class PlaylistCancionSerializer(serializers.ModelSerializer):
    cancion_titulo = serializers.CharField(source='cancion.titulo', read_only=True)
    playlist_titulo = serializers.CharField(source='playlist.titulo', read_only=True)
    
    class Meta:
        model = PlaylistCancion
        fields = '__all__'

class InteraccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaccion
        fields = '__all__'
