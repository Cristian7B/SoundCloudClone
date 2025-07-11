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
        fields = ['titulo', 'descripcion', 'imagen_url', 'es_publica', 'usuario_id']

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

class InteraccionCreateSerializer(serializers.Serializer):
    """
    Serializer para crear interacciones (like, repost, follow)
    """
    tipo = serializers.ChoiceField(
        choices=Interaccion.TIPO_CHOICES,
        help_text="Tipo de interacción: like, repost, follow"
    )
    cancion_id = serializers.IntegerField(
        required=False, 
        help_text="ID de la canción (requerido para like/repost de canción)"
    )
    playlist_id = serializers.IntegerField(
        required=False,
        help_text="ID de la playlist (requerido para like/repost de playlist)"
    )
    usuario_objetivo_id = serializers.IntegerField(
        required=False,
        help_text="ID del usuario a seguir (requerido para follow)"
    )
    usuario_id = serializers.IntegerField(
        required=False,
        help_text="ID del usuario que hace la interacción (solo para testing)"
    )
    
    def validate(self, attrs):
        tipo = attrs.get('tipo')
        cancion_id = attrs.get('cancion_id')
        playlist_id = attrs.get('playlist_id')
        usuario_objetivo_id = attrs.get('usuario_objetivo_id')
        
        # Validar que se proporcione el campo correcto según el tipo
        if tipo in ['like', 'repost']:
            if not cancion_id and not playlist_id:
                raise serializers.ValidationError(
                    "Para like/repost debe proporcionar cancion_id o playlist_id"
                )
            if cancion_id and playlist_id:
                raise serializers.ValidationError(
                    "Para like/repost debe proporcionar solo cancion_id O playlist_id, no ambos"
                )
        elif tipo == 'follow':
            if not usuario_objetivo_id:
                raise serializers.ValidationError(
                    "Para follow debe proporcionar usuario_objetivo_id"
                )
            if cancion_id or playlist_id:
                raise serializers.ValidationError(
                    "Para follow no debe proporcionar cancion_id ni playlist_id"
                )
        
        # Validar que los objetos existen
        if cancion_id and not Cancion.objects.filter(pk=cancion_id).exists():
            raise serializers.ValidationError("La canción no existe")
        
        if playlist_id and not Playlist.objects.filter(pk=playlist_id).exists():
            raise serializers.ValidationError("La playlist no existe")
        
        return attrs

class InteraccionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer con información detallada de las interacciones
    """
    cancion_titulo = serializers.CharField(source='cancion.titulo', read_only=True)
    playlist_titulo = serializers.CharField(source='playlist.titulo', read_only=True)
    
    class Meta:
        model = Interaccion
        fields = '__all__'
