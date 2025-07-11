from rest_framework import serializers
from .models import Cancion, Playlist, Album, PlaylistCancion, Interaccion


class AlbumSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Album.
    Serializa todos los campos del modelo Album.
    """

    class Meta:
        model = Album
        fields = '__all__'


class CancionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Cancion.
    Incluye todos los campos del modelo más el título del álbum asociado.

    Atributos:
        album_titulo: Campo de solo lectura que muestra el título del álbum al que pertenece la canción
    """
    album_titulo = serializers.CharField(source='album.titulo', read_only=True)

    class Meta:
        model = Cancion
        fields = '__all__'


class CancionCreateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para la creación de canciones.
    Solo incluye los campos necesarios para crear una nueva canción.

    Campos:
        titulo: Título de la canción
        descripcion: Descripción de la canción
        archivo_url: URL del archivo de audio
        imagen_url: URL de la imagen de portada
        duracion: Duración de la canción
        genero: Género musical
        album: ID del álbum al que pertenece
    """

    class Meta:
        model = Cancion
        fields = ['titulo', 'descripcion', 'archivo_url', 'imagen_url', 'duracion', 'genero', 'album']


class PlaylistSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Playlist.
    Incluye todos los campos del modelo más campos calculados.

    Atributos:
        total_canciones: Número total de canciones en la playlist
        canciones: Lista de canciones ordenadas según su posición en la playlist
    """
    total_canciones = serializers.SerializerMethodField()
    canciones = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = '__all__'

    def get_total_canciones(self, obj):
        """
        Calcula el número total de canciones en la playlist.

        Args:
            obj: Instancia de Playlist

        Returns:
            int: Número total de canciones
        """
        return obj.canciones.count()

    def get_canciones(self, obj):
        """
        Obtiene la lista ordenada de canciones en la playlist.

        Args:
            obj: Instancia de Playlist

        Returns:
            list: Lista serializada de canciones
        """
        playlist_canciones = PlaylistCancion.objects.filter(playlist=obj).order_by('orden')
        canciones = [pc.cancion for pc in playlist_canciones]
        return CancionSerializer(canciones, many=True).data


class PlaylistCreateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para la creación de playlists.

    Campos:
        titulo: Título de la playlist
        descripcion: Descripción de la playlist
        imagen_url: URL de la imagen de portada
        usuario_id: ID del usuario creador
        es_publica: Indica si la playlist es pública
    """

    class Meta:
        model = Playlist
        fields = ['titulo', 'descripcion', 'imagen_url', 'usuario_id', 'es_publica']


class PlaylistCancionSerializer(serializers.ModelSerializer):
    """
    Serializador para la relación entre Playlist y Cancion.
    Incluye campos adicionales con información de la canción y playlist.

    Atributos:
        cancion_titulo: Título de la canción (solo lectura)
        playlist_titulo: Título de la playlist (solo lectura)
    """
    cancion_titulo = serializers.CharField(source='cancion.titulo', read_only=True)
    playlist_titulo = serializers.CharField(source='playlist.titulo', read_only=True)

    class Meta:
        model = PlaylistCancion
        fields = '__all__'


class PlaylistAgregarCancionSerializer(serializers.Serializer):
    """
    Serializador específico para agregar canciones a playlists.

    Campos:
        cancion_id: ID de la canción a agregar
        orden: Posición en la playlist (opcional)
        usuario_id: ID del usuario (para testing)
    """
    cancion_id = serializers.IntegerField(help_text="ID de la canción a agregar")
    orden = serializers.IntegerField(required=False, help_text="Posición en la playlist (opcional)")
    usuario_id = serializers.IntegerField(required=False, help_text="ID del usuario (solo para testing)")

    def validate_cancion_id(self, value):
        """
        Valida que la canción exista en la base de datos.

        Args:
            value: ID de la canción

        Returns:
            int: ID de la canción si es válido

        Raises:
            ValidationError: Si la canción no existe
        """
        if not Cancion.objects.filter(pk=value).exists():
            raise serializers.ValidationError("La canción no existe")
        return value


class InteraccionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Interaccion.
    Serializa todos los campos del modelo de interacciones de usuarios con canciones.
    """

    class Meta:
        model = Interaccion
        fields = '__all__'