"""
Data models for music content persistence in the SoundCloud clone.

This module defines the core data models for managing music content including
albums, songs, playlists, and user interactions. The models are designed to
support a comprehensive music streaming platform with social features.

Models:
    Album: Represents music albums with metadata and user association
    Cancion: Represents individual songs with media files and statistics
    Playlist: Represents user-created playlists with privacy settings
    PlaylistCancion: Many-to-many relationship between playlists and songs
    Interaccion: Tracks user interactions (likes, reposts, follows)

Features:
    - Hierarchical content organization (albums → songs)
    - User-generated playlists with custom ordering
    - Social interactions tracking with engagement metrics
    - Flexible content management with optional associations
    - Comprehensive metadata support for rich content display

Database Design:
    - Normalized structure with proper foreign key relationships
    - Integer user IDs for flexible user model integration
    - Automatic timestamp tracking for audit trails
    - Unique constraints to prevent duplicate interactions
    - Optimized indexing through ordering specifications

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.db import models
from django.conf import settings


class Album(models.Model):
    """
    Model representing a music album.
    
    Albums serve as containers for organizing songs into cohesive collections.
    Each album is owned by a user and can contain multiple songs. Albums include
    metadata for rich content display and discovery.
    
    Attributes:
        album_id (AutoField): Primary key for unique album identification
        titulo (CharField): Album title/name (max 255 characters)
        descripcion (TextField): Optional detailed album description
        imagen_url (URLField): Optional album cover image URL
        usuario_id (IntegerField): ID of the user who owns this album
        created_at (DateTimeField): Timestamp when album was created
        updated_at (DateTimeField): Timestamp when album was last modified
    
    Relationships:
        - One-to-Many with Cancion (songs can belong to an album)
        - Indirect relationship with User through usuario_id
    
    Meta Configuration:
        - Database table: 'albums'
        - Default ordering: Newest first (-created_at)
    
    Methods:
        __str__(): Returns album title for string representation
    
    Example:
        album = Album.objects.create(
            titulo="My First Album",
            descripcion="Collection of my best songs",
            usuario_id=1,
            imagen_url="https://example.com/album-cover.jpg"
        )
    
    Note:
        Uses integer user ID instead of foreign key for flexibility
        in user model management across different applications.
    """
    album_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    usuario_id = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the album."""
        return self.titulo

    class Meta:
        db_table = 'albums'
        ordering = ['-created_at']


class Cancion(models.Model):
    """
    Model representing an individual song/track.
    
    Songs are the core content units of the platform. Each song contains
    audio content, metadata, and engagement statistics. Songs can optionally
    belong to albums and participate in social interactions.
    
    Attributes:
        cancion_id (AutoField): Primary key for unique song identification
        titulo (CharField): Song title/name (max 255 characters)
        descripcion (TextField): Optional detailed song description
        archivo_url (URLField): Required URL to the audio file
        imagen_url (URLField): Optional song cover/thumbnail image URL
        duracion (DurationField): Optional song duration/length
        genero (CharField): Optional genre classification (max 100 chars)
        usuario_id (IntegerField): ID of the user who uploaded this song
        album (ForeignKey): Optional album this song belongs to
        reproducciones (IntegerField): Number of times song has been played
        likes_count (IntegerField): Number of likes this song has received
        reposts_count (IntegerField): Number of times song has been reposted
        created_at (DateTimeField): Timestamp when song was uploaded
        updated_at (DateTimeField): Timestamp when song was last modified
    
    Relationships:
        - Many-to-One with Album (song can belong to one album)
        - Many-to-Many with Playlist through PlaylistCancion
        - One-to-Many with Interaccion (interactions on this song)
        - Indirect relationship with User through usuario_id
    
    Meta Configuration:
        - Database table: 'canciones'
        - Default ordering: Newest first (-created_at)
    
    Methods:
        __str__(): Returns song title for string representation
    
    Example:
        cancion = Cancion.objects.create(
            titulo="My New Song",
            archivo_url="https://example.com/audio.mp3",
            usuario_id=1,
            genero="Pop",
            duracion=timedelta(minutes=3, seconds=45)
        )
    
    Statistics Tracking:
        - Engagement metrics (likes, reposts) are denormalized for performance
        - Playback count tracks user engagement and popularity
        - Metrics can be updated through dedicated endpoints
    """
    cancion_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo_url = models.URLField()
    imagen_url = models.URLField(blank=True, null=True)
    duracion = models.DurationField(null=True, blank=True)
    genero = models.CharField(max_length=100, blank=True, null=True)
    usuario_id = models.IntegerField()  # User reference by ID
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='canciones')
    reproducciones = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    reposts_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the song."""
        return self.titulo

    class Meta:
        db_table = 'canciones'
        ordering = ['-created_at']


class Playlist(models.Model):
    """
    Model representing a user-created playlist.
    
    Playlists allow users to organize songs into custom collections.
    They support privacy settings, custom ordering, and social interactions.
    Playlists can contain songs from different users and albums.
    
    Attributes:
        playlist_id (AutoField): Primary key for unique playlist identification
        titulo (CharField): Playlist title/name (max 255 characters)
        descripcion (TextField): Optional detailed playlist description
        imagen_url (URLField): Optional playlist cover image URL
        usuario_id (IntegerField): ID of the user who created this playlist
        es_publica (BooleanField): Whether playlist is publicly visible
        created_at (DateTimeField): Timestamp when playlist was created
        updated_at (DateTimeField): Timestamp when playlist was last modified
    
    Relationships:
        - Many-to-Many with Cancion through PlaylistCancion
        - One-to-Many with Interaccion (interactions on this playlist)
        - Indirect relationship with User through usuario_id
    
    Meta Configuration:
        - Database table: 'playlists'
        - Default ordering: Newest first (-created_at)
    
    Methods:
        __str__(): Returns playlist title for string representation
    
    Privacy Features:
        - Public playlists are visible to all users
        - Private playlists are only visible to the creator
        - Privacy setting affects search and discovery features
    
    Example:
        playlist = Playlist.objects.create(
            titulo="My Favorites",
            descripcion="Songs I love listening to",
            usuario_id=1,
            es_publica=True
        )
    """
    playlist_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    usuario_id = models.IntegerField()  
    es_publica = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the playlist."""
        return self.titulo

    class Meta:
        db_table = 'playlists'
        ordering = ['-created_at']


class PlaylistCancion(models.Model):
    """
    Model representing the many-to-many relationship between playlists and songs.
    
    This model handles the association between playlists and songs with additional
    metadata including custom ordering and addition timestamps. Supports manual
    song reordering within playlists for personalized organization.
    
    Attributes:
        playlist (ForeignKey): Reference to the playlist containing the song
        cancion (ForeignKey): Reference to the song included in the playlist
        orden (IntegerField): Position/order of song within the playlist
        added_at (DateTimeField): Timestamp when song was added to playlist
    
    Relationships:
        - Many-to-One with Playlist (multiple songs per playlist)
        - Many-to-One with Cancion (song can be in multiple playlists)
    
    Meta Configuration:
        - Database table: 'playlist_canciones'
        - Unique constraint: (playlist, cancion) prevents duplicates
        - Default ordering: By orden field, then by added_at
    
    Methods:
        __str__(): Returns playlist and song titles for identification
    
    Ordering Features:
        - Manual ordering support through orden field
        - Automatic ordering by addition time as fallback
        - Supports playlist reorganization through API endpoints
    
    Example:
        PlaylistCancion.objects.create(
            playlist=playlist_instance,
            cancion=song_instance,
            orden=1  # First song in playlist
        )
    
    Note:
        The unique_together constraint ensures a song can only appear
        once in any given playlist, preventing accidental duplicates.
    """
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='canciones')
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name='playlists')
    orden = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'playlist_canciones'
        unique_together = ('playlist', 'cancion')
        ordering = ['orden', 'added_at']

    def __str__(self):
        """Return string representation showing playlist and song relationship."""
        return f'{self.playlist.titulo} - {self.cancion.titulo}'


class Interaccion(models.Model):
    """
    Model representing user interactions with content and other users.
    
    Tracks social interactions including likes, reposts, and follows.
    Supports interactions with songs, playlists, and user-to-user relationships.
    Provides the foundation for social features and engagement analytics.
    
    Interaction Types:
        - 'like': User likes a song or playlist
        - 'repost': User reposts/shares a song or playlist
        - 'follow': User follows another user
    
    Attributes:
        usuario_id (IntegerField): ID of the user performing the interaction
        cancion (ForeignKey): Optional song being interacted with
        playlist (ForeignKey): Optional playlist being interacted with
        usuario_objetivo_id (IntegerField): Optional target user ID for follows
        tipo (CharField): Type of interaction (like/repost/follow)
        created_at (DateTimeField): Timestamp when interaction occurred
    
    Relationships:
        - Many-to-One with Cancion (multiple interactions per song)
        - Many-to-One with Playlist (multiple interactions per playlist)
        - Indirect relationships with User through usuario_id and usuario_objetivo_id
    
    Meta Configuration:
        - Database table: 'interacciones'
        - Unique constraints prevent duplicate interactions
        - Default ordering: Newest first (-created_at)
    
    Methods:
        __str__(): Returns human-readable interaction description
    
    Unique Constraints:
        - (usuario_id, cancion, tipo): Prevents duplicate song interactions
        - (usuario_id, playlist, tipo): Prevents duplicate playlist interactions
        - (usuario_id, usuario_objetivo_id, tipo): Prevents duplicate follows
    
    Example:
        # User likes a song
        Interaccion.objects.create(
            usuario_id=1,
            cancion=song_instance,
            tipo='like'
        )
        
        # User follows another user
        Interaccion.objects.create(
            usuario_id=1,
            usuario_objetivo_id=2,
            tipo='follow'
        )
    
    Analytics Usage:
        - Track user engagement patterns
        - Generate recommendation algorithms
        - Calculate content popularity metrics
        - Build social network graphs
    """
    TIPO_CHOICES = [
        ('like', 'Like'),
        ('repost', 'Repost'),
        ('follow', 'Follow'),
    ]
    
    usuario_id = models.IntegerField()  
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, null=True, blank=True, related_name='interacciones')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, blank=True, related_name='interacciones')
    usuario_objetivo_id = models.IntegerField(null=True, blank=True)  # For follows
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'interacciones'
        unique_together = [
            ('usuario_id', 'cancion', 'tipo'),
            ('usuario_id', 'playlist', 'tipo'),
            ('usuario_id', 'usuario_objetivo_id', 'tipo'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        """Return human-readable description of the interaction."""
        if self.cancion:
            return f'User {self.usuario_id} {self.tipo} {self.cancion.titulo}'
        elif self.playlist:
            return f'User {self.usuario_id} {self.tipo} {self.playlist.titulo}'
        else:
            return f'User {self.usuario_id} {self.tipo} User {self.usuario_objetivo_id}'
