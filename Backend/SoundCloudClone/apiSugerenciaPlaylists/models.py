"""
Data models for playlist recommendation and discovery system.

This module defines the models that power the playlist recommendation engine,
including trending playlists, similarity calculations, personalized recommendations,
and category-based playlist organization. The system provides intelligent playlist
discovery based on user behavior, content analysis, and social patterns.

Models:
    PlaylistTendencia: Tracks trending playlists with scoring algorithms
    SimilitudPlaylists: Calculates and stores playlist similarity metrics
    RecomendacionPlaylist: Manages personalized playlist recommendations
    CategoriasPlaylist: Defines playlist categories and classification system
    PlaylistCategoria: Many-to-many relationship between playlists and categories

Features:
    - Trending playlist identification and scoring
    - Content-based and collaborative filtering for similarities
    - Personalized recommendation engine with multiple reasoning types
    - Comprehensive category system for playlist organization
    - User interaction tracking for recommendation optimization
    - Automatic and manual playlist categorization

Recommendation Algorithms:
    - Content-based filtering using shared songs
    - Collaborative filtering based on user behavior
    - Trending analysis with time-decay scoring
    - Category-based recommendations
    - Social influence from followed users

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.db import models


class PlaylistTendencia(models.Model):
    """
    Model for tracking and scoring trending playlists.
    
    Identifies playlists that are gaining popularity based on various metrics
    including recent plays, new followers, and algorithmic scoring. Supports
    multiple trending categories for diverse content discovery.
    
    Attributes:
        playlist_id (IntegerField): Reference to the trending playlist
        titulo (CharField): Cached playlist title for performance
        usuario_creador_id (IntegerField): ID of the playlist creator
        reproducciones_ultima_semana (IntegerField): Recent play count
        nuevos_seguidores (IntegerField): New follower count in recent period
        puntuacion_tendencia (FloatField): Calculated trending score
        categoria (CharField): Type of trending (nueva, viral, genero, etc.)
        activa_en_tendencias (BooleanField): Whether currently trending
        fecha_ingreso_tendencia (DateTimeField): When it started trending
        ultima_actualizacion (DateTimeField): Last score update timestamp
    
    Trending Categories:
        - nueva: New and popular playlists
        - viral: Rapidly spreading playlists
        - genero: Popular within specific genres
        - region: Geographically popular playlists
        - editorial: Curated editorial selections
    
    Scoring Algorithm:
        - Weighted combination of plays, followers, and engagement
        - Time decay for recent activity emphasis
        - Category-specific scoring adjustments
        - Periodic recalculation for freshness
    
    Meta Configuration:
        - Database table: 'playlist_tendencias'
        - Ordering: By trending score and entry date (highest first)
        - Unique constraint on playlist_id to prevent duplicates
    
    Methods:
        __str__(): Returns trending playlist identification string
    
    Example:
        trending = PlaylistTendencia.objects.create(
            playlist_id=123,
            titulo="Hot New Hits",
            usuario_creador_id=1,
            categoria='nueva',
            puntuacion_tendencia=8.5
        )
    
    Use Cases:
        - Trending playlist discovery sections
        - Homepage featured content
        - Category-specific trending lists
        - Analytics and reporting dashboards
    """
    playlist_id = models.IntegerField(unique=True)  
    titulo = models.CharField(max_length=255)  
    usuario_creador_id = models.IntegerField()  
    reproducciones_ultima_semana = models.IntegerField(default=0)
    nuevos_seguidores = models.IntegerField(default=0)
    puntuacion_tendencia = models.FloatField(default=0.0)
    categoria = models.CharField(max_length=50, choices=[
        ('nueva', 'Nueva y Popular'),
        ('viral', 'Viral'),
        ('genero', 'Popular en Género'),
        ('region', 'Popular en Región'),
        ('editorial', 'Selección Editorial'),
    ])
    activa_en_tendencias = models.BooleanField(default=True)
    fecha_ingreso_tendencia = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'playlist_tendencias'
        ordering = ['-puntuacion_tendencia', '-fecha_ingreso_tendencia']

    def __str__(self):
        """Return string representation of trending playlist."""
        return f"Trending: {self.titulo} ({self.categoria})"


class SimilitudPlaylists(models.Model):
    """
    Model for calculating and storing playlist similarity metrics.
    
    Computes and maintains similarity scores between playlists using multiple
    algorithms including content-based analysis (shared songs) and collaborative
    filtering (common users). Enables playlist recommendations based on
    similarity patterns.
    
    Attributes:
        playlist_a_id (IntegerField): First playlist in comparison pair
        playlist_b_id (IntegerField): Second playlist in comparison pair
        similitud_contenido (FloatField): Content-based similarity score
        similitud_usuarios (FloatField): User-based similarity score
        similitud_total (FloatField): Combined similarity score
        canciones_comunes (IntegerField): Number of shared songs
        usuarios_comunes (IntegerField): Number of shared users/followers
        calculada_en (DateTimeField): Last calculation timestamp
    
    Similarity Algorithms:
        - Content Similarity: Jaccard coefficient of shared songs
        - User Similarity: Overlap of users who follow both playlists
        - Combined Score: Weighted average of content and user similarities
        - Threshold filtering: Only stores significant similarities
    
    Calculation Process:
        1. Identify playlists with sufficient overlap
        2. Calculate content similarity using song intersection
        3. Calculate user similarity using follower intersection
        4. Combine scores with configurable weights
        5. Store only above-threshold similarities
    
    Meta Configuration:
        - Database table: 'similitud_playlists'
        - Unique constraint: (playlist_a_id, playlist_b_id)
        - Ordering: By total similarity (highest first)
    
    Methods:
        __str__(): Returns similarity pair identification string
    
    Performance Considerations:
        - Batch calculation for efficiency
        - Incremental updates for new playlists
        - Periodic recalculation for accuracy
        - Index optimization for fast retrieval
    
    Example:
        similarity = SimilitudPlaylists.objects.create(
            playlist_a_id=1,
            playlist_b_id=2,
            similitud_contenido=0.75,
            similitud_usuarios=0.60,
            similitud_total=0.70,
            canciones_comunes=15,
            usuarios_comunes=8
        )
    
    Use Cases:
        - "Similar playlists" recommendations
        - Content discovery algorithms
        - Playlist clustering analysis
        - Recommendation engine training data
    """
    playlist_a_id = models.IntegerField()
    playlist_b_id = models.IntegerField()
    similitud_contenido = models.FloatField(default=0.0)  # Based on shared songs
    similitud_usuarios = models.FloatField(default=0.0)   # Based on shared followers
    similitud_total = models.FloatField(default=0.0)      # Combined score
    canciones_comunes = models.IntegerField(default=0)
    usuarios_comunes = models.IntegerField(default=0)
    calculada_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'similitud_playlists'
        unique_together = ('playlist_a_id', 'playlist_b_id')
        ordering = ['-similitud_total']

    def __str__(self):
        """Return string representation of playlist similarity."""
        return f"Similitud Playlists {self.playlist_a_id}-{self.playlist_b_id}: {self.similitud_total}"


class RecomendacionPlaylist(models.Model):
    """
    Model for managing personalized playlist recommendations.
    
    Stores and tracks playlist recommendations for individual users with
    detailed reasoning, scoring, and interaction tracking. Supports multiple
    recommendation strategies and user feedback collection for algorithm
    improvement.
    
    Attributes:
        usuario_id (IntegerField): Target user for the recommendation
        playlist_recomendada_id (IntegerField): Recommended playlist ID
        razon_recomendacion (CharField): Reason category for recommendation
        puntuacion_recomendacion (FloatField): Confidence score
        mostrada_al_usuario (BooleanField): Whether shown to user
        interaccion_usuario (CharField): User's response to recommendation
        fecha_recomendacion (DateTimeField): When recommendation was created
        fecha_interaccion (DateTimeField): When user interacted
    
    Recommendation Reasons:
        - gustos_similares: Based on user's listening patterns
        - artista_seguido: Contains artists user follows
        - genero_favorito: Matches user's preferred genres
        - amigos: Popular among user's social connections
        - tendencia: Currently trending playlists
        - nueva: New content from followed artists
    
    User Interactions:
        - vista: User viewed the recommendation
        - reproducida: User played songs from playlist
        - seguida: User followed the recommended playlist
        - ignorada: User dismissed the recommendation
    
    Recommendation Pipeline:
        1. Generate candidates using multiple algorithms
        2. Score and rank recommendations
        3. Filter for diversity and novelty
        4. Store top recommendations for user
        5. Track user interactions for feedback
    
    Meta Configuration:
        - Database table: 'recomendaciones_playlists'
        - Unique constraint: (usuario_id, playlist_recomendada_id)
        - Ordering: By recommendation score and date
    
    Methods:
        __str__(): Returns recommendation identification string
    
    Privacy Considerations:
        - Only recommends public playlists
        - Respects user privacy settings
        - Anonymous usage analytics only
    
    Example:
        recommendation = RecomendacionPlaylist.objects.create(
            usuario_id=1,
            playlist_recomendada_id=123,
            razon_recomendacion='gustos_similares',
            puntuacion_recomendacion=0.85
        )
    
    Use Cases:
        - Personalized homepage recommendations
        - Discovery feed generation
        - Email/notification recommendations
        - A/B testing different algorithms
        - User feedback collection
    """
    usuario_id = models.IntegerField()
    playlist_recomendada_id = models.IntegerField()
    razon_recomendacion = models.CharField(max_length=100, choices=[
        ('gustos_similares', 'Basado en tus gustos'),
        ('artista_seguido', 'Contiene artistas que sigues'),
        ('genero_favorito', 'De tu género favorito'),
        ('amigos', 'Popular entre tus amigos'),
        ('tendencia', 'En tendencia'),
        ('nueva', 'Nueva de artista que sigues'),
    ])
    puntuacion_recomendacion = models.FloatField()
    mostrada_al_usuario = models.BooleanField(default=False)
    interaccion_usuario = models.CharField(max_length=20, choices=[
        ('vista', 'Vista'),
        ('reproducida', 'Reproducida'),
        ('seguida', 'Seguida'),
        ('ignorada', 'Ignorada'),
    ], null=True, blank=True)
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    fecha_interaccion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'recomendaciones_playlists'
        unique_together = ('usuario_id', 'playlist_recomendada_id')
        ordering = ['-puntuacion_recomendacion', '-fecha_recomendacion']

    def __str__(self):
        """Return string representation of playlist recommendation."""
        return f"User {self.usuario_id}: Playlist {self.playlist_recomendada_id} ({self.razon_recomendacion})"


class CategoriasPlaylist(models.Model):
    """
    Model for defining playlist categories and classification system.
    
    Provides a comprehensive categorization system for playlists including
    musical genres, moods, activities, and custom categories. Supports
    visual customization and hierarchical organization for enhanced
    user experience and content discovery.
    
    Attributes:
        nombre (CharField): Category name (unique identifier)
        descripcion (TextField): Detailed category description
        color_hex (CharField): UI color code for visual consistency
        icono (CharField): Icon identifier for category representation
        es_genero_musical (BooleanField): Whether category represents music genre
        es_estado_animo (BooleanField): Whether category represents mood
        es_actividad (BooleanField): Whether category represents activity
        activa (BooleanField): Whether category is currently active
        orden_display (IntegerField): Sort order for UI display
        created_at (DateTimeField): Category creation timestamp
    
    Category Types:
        - Musical Genres: Rock, Pop, Jazz, Electronic, etc.
        - Moods: Happy, Sad, Energetic, Relaxing, etc.
        - Activities: Workout, Study, Party, Sleep, etc.
        - Custom: User-defined or editorial categories
    
    Visual Customization:
        - Color codes for consistent UI theming
        - Icon support for visual category identification
        - Display order control for logical organization
        - Active/inactive status for content management
    
    Meta Configuration:
        - Database table: 'categorias_playlist'
        - Unique constraint on category name
        - Ordering: By display order, then alphabetically
    
    Methods:
        __str__(): Returns category name
    
    Usage Patterns:
        - Automatic categorization based on playlist content
        - Manual assignment by playlist creators
        - Machine learning classification
        - Editorial curation and organization
    
    Example:
        category = CategoriasPlaylist.objects.create(
            nombre="Workout",
            descripcion="High-energy music for exercise",
            color_hex="#FF6B35",
            icono="fitness",
            es_actividad=True,
            orden_display=10
        )
    
    Use Cases:
        - Category-based playlist browsing
        - Filtered search and discovery
        - Personalized category recommendations
        - Content organization and curation
        - UI theme and visual consistency
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    color_hex = models.CharField(max_length=7, default='#000000')  # UI color
    icono = models.CharField(max_length=50, blank=True, null=True)
    es_genero_musical = models.BooleanField(default=False)
    es_estado_animo = models.BooleanField(default=False)
    es_actividad = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)
    orden_display = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias_playlist'
        ordering = ['orden_display', 'nombre']

    def __str__(self):
        """Return string representation of category."""
        return self.nombre


class PlaylistCategoria(models.Model):
    """
    Model for many-to-many relationship between playlists and categories.
    
    Manages the association between playlists and their categories with
    additional metadata including relevance scoring, assignment tracking,
    and automated categorization support. Enables flexible playlist
    organization and category-based discovery.
    
    Attributes:
        playlist_id (IntegerField): Reference to categorized playlist
        categoria (ForeignKey): Reference to assigned category
        relevancia (FloatField): How relevant this category is to playlist
        asignada_automaticamente (BooleanField): Whether auto-assigned
        asignada_en (DateTimeField): When category was assigned
    
    Relevance Scoring:
        - 1.0: Perfect match (e.g., all songs match genre)
        - 0.7-0.9: Strong match (most songs match)
        - 0.4-0.6: Moderate match (some songs match)
        - 0.1-0.3: Weak match (few songs match)
    
    Assignment Methods:
        - Automatic: Algorithm-based categorization
        - Manual: User or editor assignment
        - Hybrid: Automatic with manual validation
        - Machine Learning: AI-powered classification
    
    Meta Configuration:
        - Database table: 'playlist_categorias'
        - Unique constraint: (playlist_id, categoria)
        - Prevents duplicate category assignments
    
    Methods:
        __str__(): Returns playlist-category relationship string
    
    Quality Control:
        - Relevance thresholds for automatic assignments
        - Manual review for editorial categories
        - User feedback for assignment accuracy
        - Periodic recalculation of relevance scores
    
    Example:
        assignment = PlaylistCategoria.objects.create(
            playlist_id=123,
            categoria=workout_category,
            relevancia=0.85,
            asignada_automaticamente=True
        )
    
    Use Cases:
        - Category-filtered playlist browsing
        - Multi-category playlist classification
        - Relevance-based search ranking
        - Automated content organization
        - Category analytics and insights
    """
    playlist_id = models.IntegerField()
    categoria = models.ForeignKey(CategoriasPlaylist, on_delete=models.CASCADE)
    relevancia = models.FloatField(default=1.0)  # Category relevance to playlist
    asignada_automaticamente = models.BooleanField(default=False)
    asignada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'playlist_categorias'
        unique_together = ('playlist_id', 'categoria')

    def __str__(self):
        """Return string representation of playlist-category relationship."""
        return f"Playlist {self.playlist_id} - {self.categoria.nombre}"
