from rest_framework import serializers
from apiPersistencia.models import Cancion, Playlist
from .models import IndicesBusqueda, HistorialBusqueda, SugerenciasBusqueda

class CancionSerializer(serializers.ModelSerializer):
    """
        Serializador para mostrar canciones en resultados de búsqueda.

        Campos:
            cancion_id (int): Identificador único de la canción
            titulo (str): Título de la canción
            archivo_url (str): URL del archivo de audio
            imagen_url (str): URL de la imagen de portada
            duracion (time): Duración de la canción
            genero (str): Género musical
            usuario_id (int): ID del creador
            reproducciones (int): Contador de reproducciones
            likes_count (int): Contador de "me gusta"
            created_at (datetime): Fecha de creación
    """
    class Meta:
        model = Cancion
        fields = ['cancion_id', 'titulo', 'archivo_url', 'imagen_url', 'duracion', 'genero', 'usuario_id', 'reproducciones', 'likes_count', 'created_at']

class PlaylistSerializer(serializers.ModelSerializer):
    """
        Serializador para mostrar playlists en resultados de búsqueda.

        Campos:
            playlist_id (int): Identificador único de la playlist
            titulo (str): Nombre de la playlist
            descripcion (str): Descripción opcional
            imagen_url (str): URL de la imagen de portada
            usuario_id (int): ID del creador
            es_publica (bool): Indica si es pública
            total_canciones (int): Número de canciones (campo calculado)
            created_at (datetime): Fecha de creación

        Métodos:
            get_total_canciones: Calcula el total de canciones en la playlist
    """
    total_canciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['playlist_id', 'titulo', 'descripcion', 'imagen_url', 'usuario_id', 'es_publica', 'total_canciones', 'created_at']
    
    def get_total_canciones(self, obj):
        return obj.canciones.count()

class IndicesBusquedaSerializer(serializers.ModelSerializer):
    """
        Serializador para los índices de búsqueda.
        Gestiona los términos indexados para búsqueda rápida.

        Campos:
            Todos los campos del modelo IndicesBusqueda
    """
    class Meta:
        model = IndicesBusqueda
        fields = '__all__'

class HistorialBusquedaSerializer(serializers.ModelSerializer):
    """
        Serializador para el historial de búsquedas.
        Registra las búsquedas realizadas por los usuarios.

        Campos:
            Todos los campos del modelo HistorialBusqueda
    """
    class Meta:
        model = HistorialBusqueda
        fields = '__all__'

class SugerenciasBusquedaSerializer(serializers.ModelSerializer):
    """
        Serializador para las sugerencias de búsqueda.
        Maneja las sugerencias automáticas basadas en búsquedas populares.

        Campos:
            Todos los campos del modelo SugerenciasBusqueda
    """
    class Meta:
        model = SugerenciasBusqueda
        fields = '__all__'
