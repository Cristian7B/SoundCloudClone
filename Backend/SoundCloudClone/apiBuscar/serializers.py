from rest_framework import serializers
from apiPersistencia.models import Cancion, Playlist
from .models import IndicesBusqueda, HistorialBusqueda, SugerenciasBusqueda

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = ['cancion_id', 'titulo', 'archivo_url', 'imagen_url', 'duracion', 'genero', 'usuario_id', 'reproducciones', 'likes_count', 'created_at']

class PlaylistSerializer(serializers.ModelSerializer):
    total_canciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['playlist_id', 'titulo', 'descripcion', 'imagen_url', 'usuario_id', 'es_publica', 'total_canciones', 'created_at']
    
    def get_total_canciones(self, obj):
        return obj.canciones.count()

class IndicesBusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicesBusqueda
        fields = '__all__'

class HistorialBusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialBusqueda
        fields = '__all__'

class SugerenciasBusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugerenciasBusqueda
        fields = '__all__'
