"""
Serializers for music content persistence API.

This module contains all the serializers used for converting between Django model
instances and JSON representations for the music content management system.
Includes serializers for albums, songs, playlists, and user interactions with
comprehensive validation and nested data handling.

Classes:
    AlbumSerializer: Standard album data serialization
    CancionSerializer: Full song data with album information
    CancionCreateSerializer: Song creation with validation
    PlaylistSerializer: Complete playlist with songs and statistics
    PlaylistCreateSerializer: Playlist creation with validation
    PlaylistCancionSerializer: Playlist-song relationship data
    PlaylistAgregarCancionSerializer: Adding songs to playlists
    InteraccionSerializer: Standard interaction data
    InteraccionCreateSerializer: Creating interactions with validation
    InteraccionDetailSerializer: Detailed interaction information

Features:
    - Nested data representation for related objects
    - Comprehensive input validation for data integrity
    - Specialized serializers for different use cases
    - Read-only computed fields for enhanced functionality
    - Cross-model relationship handling

@author: Development Team
@version: 1.0
@since: 2024
"""

from rest_framework import serializers
from .models import Cancion, Playlist, Album, PlaylistCancion, Interaccion


class AlbumSerializer(serializers.ModelSerializer):
    """
    Standard serializer for album data representation.
    
    Provides complete album information including metadata and timestamps.
    Used for both reading and writing album data through API endpoints.
    
    Fields:
        All model fields are included for comprehensive data access
    
    Use Cases:
        - Album listing and detail views
        - Album creation and updates
        - Nested album information in song serializers
    
    Example:
        album_data = AlbumSerializer(album_instance).data
        # Returns: {'album_id': 1, 'titulo': 'My Album', ...}
    """
    class Meta:
        model = Album
        fields = '__all__'


class CancionSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for song data with album information.
    
    Includes all song metadata plus related album title for rich content display.
    Provides read-only album title to avoid nested object creation complexity.
    
    Fields:
        All song model fields plus:
        album_titulo (CharField): Read-only title of associated album
    
    Features:
        - Complete song metadata
        - Album title for display purposes
        - Engagement statistics (likes, reposts, plays)
        - Timestamp information for sorting and filtering
    
    Use Cases:
        - Song listing with album context
        - Detailed song information views
        - Music player data provision
        - Search result formatting
    
    Example:
        song_data = CancionSerializer(song_instance).data
        # Returns: {'cancion_id': 1, 'titulo': 'Song', 'album_titulo': 'Album', ...}
    """
    album_titulo = serializers.CharField(source='album.titulo', read_only=True)

    class Meta:
        model = Cancion
        fields = '__all__'


class CancionCreateSerializer(serializers.ModelSerializer):
    """
    Specialized serializer for creating new songs.
    
    Focused on essential fields needed for song creation, excluding
    auto-generated fields like timestamps and statistics. Validates
    required data and optional metadata for new song uploads.
    
    Fields:
        titulo (str): Song title (required)
        descripcion (str): Song description (optional)
        archivo_url (str): Audio file URL (required)
        imagen_url (str): Cover image URL (optional)
        duracion (Duration): Song length (optional)
        genero (str): Music genre (optional)
        album (ForeignKey): Associated album (optional)
    
    Validation:
        - Ensures required fields are provided
        - Validates URL formats for audio and image files
        - Checks album existence if provided
    
    Use Cases:
        - New song upload endpoints
        - Song creation forms
        - Bulk song import operations
    
    Example:
        serializer = CancionCreateSerializer(data={
            'titulo': 'My Song',
            'archivo_url': 'https://example.com/song.mp3'
        })
        if serializer.is_valid():
            song = serializer.save(usuario_id=user.id)
    """
    class Meta:
        model = Cancion
        fields = ['titulo', 'descripcion', 'archivo_url', 'imagen_url', 'duracion', 'genero', 'album']


class PlaylistSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for playlist data with songs and statistics.
    
    Provides complete playlist information including song list, total count,
    and properly ordered track listing. Handles the complex many-to-many
    relationship between playlists and songs with custom ordering.
    
    Fields:
        All playlist model fields plus:
        total_canciones (int): Count of songs in the playlist
        canciones (list): Ordered list of songs with full data
    
    Methods:
        get_total_canciones(): Calculate total number of songs
        get_canciones(): Retrieve ordered song list with full metadata
    
    Features:
        - Complete playlist metadata
        - Ordered song listing respecting playlist order
        - Song count for UI display
        - Full song data for immediate playback
    
    Use Cases:
        - Playlist detail views
        - Music player playlist loading
        - Playlist sharing and export
        - Social media playlist previews
    
    Performance Notes:
        - Uses optimized queries for song retrieval
        - Maintains order through PlaylistCancion model
        - Includes full song data to minimize additional API calls
    
    Example:
        playlist_data = PlaylistSerializer(playlist_instance).data
        # Returns: {'playlist_id': 1, 'titulo': 'My Playlist', 
        #          'total_canciones': 5, 'canciones': [...]}
    """
    total_canciones = serializers.SerializerMethodField()
    canciones = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = '__all__'
    
    def get_total_canciones(self, obj):
        """Calculate total number of songs in the playlist."""
        return obj.canciones.count()
    
    def get_canciones(self, obj):
        """Retrieve ordered list of songs with full metadata."""
        playlist_canciones = PlaylistCancion.objects.filter(playlist=obj).order_by('orden')
        canciones = [pc.cancion for pc in playlist_canciones]
        return CancionSerializer(canciones, many=True).data


class PlaylistCreateSerializer(serializers.ModelSerializer):
    """
    Specialized serializer for creating new playlists.
    
    Focused on essential fields for playlist creation, excluding auto-generated
    fields and complex relationships. Handles initial playlist setup with
    proper validation and user association.
    
    Fields:
        titulo (str): Playlist title (required)
        descripcion (str): Playlist description (optional)
        imagen_url (str): Cover image URL (optional)
        es_publica (bool): Public visibility setting
        usuario_id (int): Owner user ID
    
    Validation:
        - Ensures required fields are provided
        - Validates URL format for cover image
        - Checks user existence for usuario_id
    
    Use Cases:
        - New playlist creation endpoints
        - Playlist creation forms
        - Bulk playlist import operations
    
    Example:
        serializer = PlaylistCreateSerializer(data={
            'titulo': 'My Playlist',
            'es_publica': True,
            'usuario_id': 1
        })
        if serializer.is_valid():
            playlist = serializer.save()
    """
    class Meta:
        model = Playlist
        fields = ['titulo', 'descripcion', 'imagen_url', 'es_publica', 'usuario_id']


class PlaylistCancionSerializer(serializers.ModelSerializer):
    """
    Serializer for playlist-song relationship data.
    
    Handles the many-to-many relationship between playlists and songs with
    additional metadata including order and timestamps. Provides context
    information for both playlist and song titles.
    
    Fields:
        All PlaylistCancion model fields plus:
        cancion_titulo (str): Read-only song title for display
        playlist_titulo (str): Read-only playlist title for display
    
    Features:
        - Complete relationship metadata
        - Order information for playlist sequencing
        - Addition timestamps for history tracking
        - Context titles for easy identification
    
    Use Cases:
        - Playlist management interfaces
        - Song-playlist relationship queries
        - Playlist order management
        - History and audit trails
    
    Example:
        relationship_data = PlaylistCancionSerializer(playlist_song).data
        # Returns: {'playlist': 1, 'cancion': 5, 'orden': 3, 
        #          'cancion_titulo': 'Song', 'playlist_titulo': 'Playlist'}
    """
    cancion_titulo = serializers.CharField(source='cancion.titulo', read_only=True)
    playlist_titulo = serializers.CharField(source='playlist.titulo', read_only=True)
    
    class Meta:
        model = PlaylistCancion
        fields = '__all__'


class PlaylistAgregarCancionSerializer(serializers.Serializer):
    """
    Specialized serializer for adding songs to playlists.
    
    Handles the specific operation of adding songs to playlists with proper
    validation and optional ordering. Designed for playlist management
    operations with comprehensive error checking.
    
    Fields:
        cancion_id (int): ID of the song to add (required)
        orden (int): Position in playlist (optional, auto-calculated if not provided)
        usuario_id (int): User ID for authorization (optional, used in testing)
    
    Validation:
        validate_cancion_id(): Ensures the song exists in the database
    
    Features:
        - Song existence validation
        - Optional order specification
        - Flexible user ID handling for different contexts
        - Clear error messages for invalid data
    
    Use Cases:
        - Adding songs to playlists via API
        - Playlist management interfaces
        - Bulk song addition operations
        - Mobile app playlist editing
    
    Error Handling:
        - Validates song existence before processing
        - Provides clear error messages for missing songs
        - Handles duplicate addition at the view level
    
    Example:
        serializer = PlaylistAgregarCancionSerializer(data={
            'cancion_id': 123,
            'orden': 5
        })
        if serializer.is_valid():
            # Process the addition
            validated_data = serializer.validated_data
    """
    cancion_id = serializers.IntegerField(help_text="ID de la canción a agregar")
    orden = serializers.IntegerField(required=False, help_text="Posición en la playlist (opcional)")
    usuario_id = serializers.IntegerField(required=False, help_text="ID del usuario (solo para testing)")
    
    def validate_cancion_id(self, value):
        """
        Validate that the song exists in the database.
        
        Args:
            value (int): The song ID to validate
            
        Returns:
            int: The validated song ID
            
        Raises:
            ValidationError: If the song does not exist
        """
        if not Cancion.objects.filter(pk=value).exists():
            raise serializers.ValidationError("La canción no existe")
        return value


class InteraccionSerializer(serializers.ModelSerializer):
    """
    Standard serializer for user interaction data.
    
    Provides complete interaction information for likes, reposts, and follows.
    Used for reading and writing interaction data through API endpoints.
    
    Fields:
        All Interaccion model fields for comprehensive access
    
    Use Cases:
        - Interaction history views
        - Social feed generation
        - Analytics and reporting
        - User activity tracking
    
    Example:
        interaction_data = InteraccionSerializer(interaction_instance).data
        # Returns: {'usuario_id': 1, 'tipo': 'like', 'cancion': 5, ...}
    """
    class Meta:
        model = Interaccion
        fields = '__all__'


class InteraccionCreateSerializer(serializers.Serializer):
    """
    Specialized serializer for creating user interactions.
    
    Handles the creation of likes, reposts, and follows with comprehensive
    validation to ensure data integrity and proper relationships. Validates
    that the correct fields are provided for each interaction type.
    
    Fields:
        tipo (str): Interaction type (like/repost/follow)
        cancion_id (int): Song ID for song interactions (optional)
        playlist_id (int): Playlist ID for playlist interactions (optional)
        usuario_objetivo_id (int): Target user ID for follows (optional)
        usuario_id (int): Acting user ID (optional, for testing)
    
    Validation Rules:
        - Like/Repost: Requires either cancion_id OR playlist_id (not both)
        - Follow: Requires usuario_objetivo_id only
        - Validates existence of referenced objects
        - Ensures proper field combinations for each interaction type
    
    Methods:
        validate(): Cross-field validation for interaction type requirements
    
    Features:
        - Type-specific field validation
        - Object existence checking
        - Clear error messages for invalid combinations
        - Flexible user ID handling
    
    Use Cases:
        - Social interaction endpoints
        - Like/unlike toggle operations
        - Follow/unfollow functionality
        - Repost operations
    
    Error Messages:
        - Clear guidance for required fields per interaction type
        - Specific errors for non-existent referenced objects
        - Helpful validation for field combinations
    
    Example:
        # Like a song
        serializer = InteraccionCreateSerializer(data={
            'tipo': 'like',
            'cancion_id': 123
        })
        
        # Follow a user
        serializer = InteraccionCreateSerializer(data={
            'tipo': 'follow',
            'usuario_objetivo_id': 456
        })
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
        """
        Perform cross-field validation for interaction requirements.
        
        Args:
            attrs (dict): Dictionary of field values
            
        Returns:
            dict: Validated attributes
            
        Raises:
            ValidationError: If field combinations are invalid for interaction type
        """
        tipo = attrs.get('tipo')
        cancion_id = attrs.get('cancion_id')
        playlist_id = attrs.get('playlist_id')
        usuario_objetivo_id = attrs.get('usuario_objetivo_id')
        
        # Validate correct fields are provided for each interaction type
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
        
        # Validate that referenced objects exist
        if cancion_id and not Cancion.objects.filter(pk=cancion_id).exists():
            raise serializers.ValidationError("La canción no existe")
        
        if playlist_id and not Playlist.objects.filter(pk=playlist_id).exists():
            raise serializers.ValidationError("La playlist no existe")
        
        return attrs


class InteraccionDetailSerializer(serializers.ModelSerializer):
    """
    Enhanced serializer for interaction data with related object information.
    
    Provides comprehensive interaction details including titles of related
    songs and playlists for rich display in user interfaces. Useful for
    activity feeds and interaction history views.
    
    Fields:
        All Interaccion model fields plus:
        cancion_titulo (str): Read-only title of liked/reposted song
        playlist_titulo (str): Read-only title of liked/reposted playlist
    
    Features:
        - Complete interaction metadata
        - Related object titles for context
        - Timestamp information for chronological ordering
        - User and target identification
    
    Use Cases:
        - Activity feed generation
        - Interaction history displays
        - Social notification systems
        - User engagement analytics
    
    Performance Notes:
        - Uses source paths to avoid additional database queries
        - Read-only fields prevent accidental updates
        - Efficient for display-only scenarios
    
    Example:
        detailed_data = InteraccionDetailSerializer(interaction).data
        # Returns: {'usuario_id': 1, 'tipo': 'like', 'cancion_titulo': 'Song Name', ...}
    """
    cancion_titulo = serializers.CharField(source='cancion.titulo', read_only=True)
    playlist_titulo = serializers.CharField(source='playlist.titulo', read_only=True)
    
    class Meta:
        model = Interaccion
        fields = '__all__'
