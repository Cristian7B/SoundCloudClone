"""
Data models for song recommendation and music discovery system.

This module defines the models that power the intelligent song recommendation
engine, including user preference tracking, listening history analysis,
song similarity calculations, and recommendation feedback systems. The models
support both collaborative and content-based filtering algorithms.

Models:
    PreferenciasUsuario: User preferences and behavioral patterns
    HistorialReproduccion: Detailed listening history for recommendation training
    SimilitudCanciones: Song-to-song similarity matrix for content-based filtering
    RecomendacionGenerada: Cached recommendations with algorithm metadata
    FeedbackRecomendacion: User feedback for recommendation algorithm improvement

Features:
    - Comprehensive user preference profiling
    - Detailed listening behavior tracking with context
    - Song similarity calculations for content-based recommendations
    - Recommendation caching for performance optimization
    - User feedback collection for algorithm learning and improvement

Recommendation Algorithms Supported:
    - Collaborative filtering based on user behavior patterns
    - Content-based filtering using song characteristics
    - Hybrid approaches combining multiple techniques
    - Context-aware recommendations using listening patterns

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.db import models


class PreferenciasUsuario(models.Model):
    """
    Model for tracking user preferences and behavioral patterns.
    
    Stores comprehensive user preference data derived from listening behavior,
    explicit feedback, and interaction patterns. Used to build user profiles
    for personalized song recommendations and content discovery.
    
    Attributes:
        usuario_id (IntegerField): Reference to user (unique per user)
        generos_favoritos (JSONField): List of preferred music genres
        artistas_seguidos (JSONField): List of followed artist IDs
        total_reproducciones (IntegerField): Total lifetime play count
        canciones_gustadas (IntegerField): Total number of liked songs
        playlists_creadas (IntegerField): Number of playlists created
        ultima_actividad (DateTimeField): Last user activity timestamp
        created_at (DateTimeField): When preferences tracking started
    
    Preference Derivation:
        - Genres extracted from listening history analysis
        - Artists identified from play frequency and explicit follows
        - Engagement metrics calculated from user interactions
        - Activity patterns tracked for recommendation timing
    
    Data Sources:
        - Listening history analysis for implicit preferences
        - Explicit user actions (likes, follows, playlists)
        - Behavioral patterns (play frequency, completion rates)
        - Social interactions (shares, reposts, comments)
    
    Meta Configuration:
        - Database table: 'preferencias_usuario'
        - Unique constraint on usuario_id (one profile per user)
    
    Methods:
        __str__(): Returns user preference identification string
    
    Privacy Considerations:
        - Aggregated data only, no individual song tracking here
        - Anonymizable for analytics and research
        - User-controlled preference management
    
    Example:
        preferences = PreferenciasUsuario.objects.create(
            usuario_id=123,
            generos_favoritos=['rock', 'pop', 'electronic'],
            artistas_seguidos=[1, 5, 12, 25],
            total_reproducciones=1250,
            canciones_gustadas=85
        )
    
    Use Cases:
        - Personalized homepage content
        - Genre-based song recommendations
        - Artist-similarity recommendations
        - User engagement analytics
        - A/B testing recommendation algorithms
    """
    usuario_id = models.IntegerField(unique=True)  # User reference by ID
    generos_favoritos = models.JSONField(default=list)  # Preferred genres list
    artistas_seguidos = models.JSONField(default=list)  # Followed artist IDs
    total_reproducciones = models.IntegerField(default=0)
    canciones_gustadas = models.IntegerField(default=0)
    playlists_creadas = models.IntegerField(default=0)
    ultima_actividad = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'preferencias_usuario'

    def __str__(self):
        """Return string representation of user preferences."""
        return f"Preferencias User {self.usuario_id}"


class HistorialReproduccion(models.Model):
    """
    Model for detailed listening history tracking.
    
    Records comprehensive listening sessions including duration, completion
    percentage, and contextual information. Used for training recommendation
    algorithms and understanding user behavior patterns.
    
    Attributes:
        usuario_id (IntegerField): Reference to listening user
        cancion_id (IntegerField): Reference to played song
        duracion_reproducida (DurationField): Actual listening duration
        porcentaje_escuchado (FloatField): Percentage of song completed
        dispositivo (CharField): Device type used for listening
        ubicacion (CharField): Location context (optional)
        hora_del_dia (TimeField): Time when listening occurred
        created_at (DateTimeField): Listening session timestamp
    
    Listening Quality Metrics:
        - Duration vs. song length for engagement measurement
        - Completion percentage for satisfaction indication
        - Skip patterns for preference learning
        - Repeat listening for strong preference signals
    
    Context Information:
        - Device type for platform-specific recommendations
        - Location for geographical pattern analysis
        - Time of day for temporal preference patterns
        - Session context for mood-based recommendations
    
    Meta Configuration:
        - Database table: 'historial_reproducciones'
        - Ordering: Most recent listening first
        - No unique constraints (allows multiple plays)
    
    Methods:
        __str__(): Returns listening session identification string
    
    Analytics Applications:
        - Skip rate analysis for recommendation quality
        - Peak listening time identification
        - Device usage pattern analysis
        - Geographic listening preference mapping
        - Engagement metric calculation
    
    Example:
        listening = HistorialReproduccion.objects.create(
            usuario_id=123,
            cancion_id=456,
            duracion_reproducida=timedelta(minutes=2, seconds=45),
            porcentaje_escuchado=85.5,
            dispositivo='mobile',
            ubicacion='home'
        )
    
    Use Cases:
        - Recommendation algorithm training data
        - User engagement analysis
        - Peak listening time optimization
        - Device-specific feature development
        - Music discovery pattern analysis
    """
    usuario_id = models.IntegerField()  # User reference by ID
    cancion_id = models.IntegerField()  # Song reference by ID
    duracion_reproducida = models.DurationField()  # Actual listening time
    porcentaje_escuchado = models.FloatField()  # Completion percentage
    dispositivo = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    hora_del_dia = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_reproducciones'
        ordering = ['-created_at']

    def __str__(self):
        """Return string representation of listening session."""
        return f"User {self.usuario_id} - Song {self.cancion_id} ({self.porcentaje_escuchado}%)"


class SimilitudCanciones(models.Model):
    """
    Model for song-to-song similarity calculations.
    
    Stores computed similarity scores between song pairs based on various
    factors including musical characteristics, user behavior patterns, and
    metadata analysis. Enables content-based recommendation algorithms.
    
    Attributes:
        cancion_a_id (IntegerField): First song in similarity pair
        cancion_b_id (IntegerField): Second song in similarity pair
        puntuacion_similitud (FloatField): Overall similarity score (0.0-1.0)
        factores_similitud (JSONField): Breakdown of similarity factors
        calculada_en (DateTimeField): When similarity was last calculated
    
    Similarity Factors:
        - Genre compatibility and overlap
        - Artist relationship and collaboration history
        - Musical characteristics (tempo, key, style)
        - User behavior patterns (often played together)
        - Playlist co-occurrence frequency
        - Social signals (shared, liked together)
    
    Scoring Algorithm:
        - Weighted combination of multiple similarity factors
        - Machine learning models for feature importance
        - User feedback integration for score refinement
        - Periodic recalculation for accuracy maintenance
    
    Meta Configuration:
        - Database table: 'similitud_canciones'
        - Unique constraint: (cancion_a_id, cancion_b_id)
        - Ordering: Highest similarity first
    
    Methods:
        __str__(): Returns song similarity identification string
    
    Performance Optimizations:
        - Batch calculation for efficiency
        - Threshold filtering (only store significant similarities)
        - Incremental updates for new songs
        - Caching for frequently accessed pairs
    
    Example:
        similarity = SimilitudCanciones.objects.create(
            cancion_a_id=123,
            cancion_b_id=456,
            puntuacion_similitud=0.85,
            factores_similitud={
                'genre': 0.9,
                'artist': 0.7,
                'tempo': 0.8,
                'user_behavior': 0.9
            }
        )
    
    Use Cases:
        - "Similar songs" recommendations
        - Radio station generation
        - Playlist continuation suggestions
        - Song discovery algorithms
        - Music analysis and research
    """
    cancion_a_id = models.IntegerField()
    cancion_b_id = models.IntegerField()
    puntuacion_similitud = models.FloatField()  # Score from 0.0 to 1.0
    factores_similitud = models.JSONField(default=dict)  # Similarity factor breakdown
    calculada_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'similitud_canciones'
        unique_together = ('cancion_a_id', 'cancion_b_id')
        ordering = ['-puntuacion_similitud']

    def __str__(self):
        """Return string representation of song similarity."""
        return f"Similitud {self.cancion_a_id}-{self.cancion_b_id}: {self.puntuacion_similitud}"


class RecomendacionGenerada(models.Model):
    """
    Model for caching generated song recommendations.
    
    Stores pre-computed song recommendations for users with algorithm metadata
    and validity periods. Improves response times and enables recommendation
    quality tracking and algorithm comparison.
    
    Attributes:
        usuario_id (IntegerField): Target user for recommendations
        canciones_recomendadas (JSONField): List of recommended song IDs
        algoritmo_usado (CharField): Algorithm used for generation
        puntuacion_confianza (FloatField): Confidence in recommendations
        valida_hasta (DateTimeField): Recommendation expiry timestamp
        generada_en (DateTimeField): When recommendations were generated
    
    Supported Algorithms:
        - collaborative: Collaborative filtering based on user behavior
        - content-based: Content similarity recommendations
        - hybrid: Combined approach using multiple techniques
        - trending: Popular and trending song recommendations
        - social: Recommendations based on social connections
    
    Caching Strategy:
        - Pre-computed recommendations for active users
        - Validity periods based on user activity frequency
        - Algorithm-specific caching policies
        - Automatic refresh for expired recommendations
    
    Meta Configuration:
        - Database table: 'recomendaciones_generadas'
        - Ordering: Most recent generation first
        - No unique constraints (allows multiple algorithm results)
    
    Methods:
        __str__(): Returns recommendation cache identification string
    
    Quality Metrics:
        - Confidence scores for recommendation ranking
        - Algorithm performance comparison
        - User interaction rate tracking
        - Recommendation freshness monitoring
    
    Example:
        recommendations = RecomendacionGenerada.objects.create(
            usuario_id=123,
            canciones_recomendadas=[456, 789, 101, 112, 131],
            algoritmo_usado='hybrid',
            puntuacion_confianza=0.78,
            valida_hasta=datetime.now() + timedelta(hours=24)
        )
    
    Use Cases:
        - Fast recommendation serving
        - Algorithm A/B testing
        - Recommendation quality analysis
        - User engagement optimization
        - Performance monitoring
    """
    usuario_id = models.IntegerField()
    canciones_recomendadas = models.JSONField(default=list)  # Recommended song IDs
    algoritmo_usado = models.CharField(max_length=50)  # Algorithm identifier
    puntuacion_confianza = models.FloatField()
    valida_hasta = models.DateTimeField()
    generada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recomendaciones_generadas'
        ordering = ['-generada_en']

    def __str__(self):
        """Return string representation of recommendation cache."""
        return f"Recomendaciones User {self.usuario_id} ({self.algoritmo_usado})"


class FeedbackRecomendacion(models.Model):
    """
    Model for collecting user feedback on song recommendations.
    
    Tracks user interactions with recommended songs to improve algorithm
    performance and personalization. Provides essential feedback loop for
    machine learning models and recommendation quality assessment.
    
    Attributes:
        usuario_id (IntegerField): User providing feedback
        cancion_recomendada_id (IntegerField): Recommended song being rated
        accion (CharField): Type of user interaction with recommendation
        tiempo_interaccion (DurationField): Duration of interaction
        created_at (DateTimeField): When feedback was recorded
    
    Feedback Types:
        - reproducida: User played the recommended song
        - gustada: User explicitly liked the recommendation
        - omitida: User skipped the recommendation
        - rechazada: User explicitly rejected the recommendation
    
    Learning Applications:
        - Algorithm parameter tuning based on feedback patterns
        - User preference refinement for personalization
        - Recommendation quality scoring and monitoring
        - A/B testing for algorithm improvements
    
    Meta Configuration:
        - Database table: 'feedback_recomendaciones'
        - Unique constraint: (usuario_id, cancion_recomendada_id)
        - Prevents duplicate feedback on same recommendation
    
    Methods:
        __str__(): Returns feedback identification string
    
    Analytics Insights:
        - Recommendation acceptance rates by algorithm
        - User satisfaction metrics calculation
        - Song popularity vs. recommendation success correlation
        - Temporal feedback pattern analysis
    
    Example:
        feedback = FeedbackRecomendacion.objects.create(
            usuario_id=123,
            cancion_recomendada_id=456,
            accion='reproducida',
            tiempo_interaccion=timedelta(minutes=2, seconds=30)
        )
    
    Use Cases:
        - Algorithm performance evaluation
        - Personalization improvement
        - Recommendation quality metrics
        - User satisfaction tracking
        - Machine learning model training
    """
    usuario_id = models.IntegerField()
    cancion_recomendada_id = models.IntegerField()
    accion = models.CharField(max_length=20, choices=[
        ('reproducida', 'Reproducida'),
        ('gustada', 'Le gustó'),
        ('omitida', 'Omitida'),
        ('rechazada', 'Rechazada'),
    ])
    tiempo_interaccion = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback_recomendaciones'
        unique_together = ('usuario_id', 'cancion_recomendada_id')

    def __str__(self):
        """Return string representation of recommendation feedback."""
        return f"User {self.usuario_id}: {self.accion} song {self.cancion_recomendada_id}"
