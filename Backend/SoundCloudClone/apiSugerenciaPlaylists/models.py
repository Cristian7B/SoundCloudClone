from django.db import models

class PlaylistTendencia(models.Model):
    """Playlists que están en tendencia"""
    playlist_id = models.IntegerField(unique=True)  # Referencia a la playlist por ID
    titulo = models.CharField(max_length=255)  # Cache del título
    usuario_creador_id = models.IntegerField()  # Referencia al creador por ID
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
        return f"Trending: {self.titulo} ({self.categoria})"

class SimilitudPlaylists(models.Model):
    """Similitud entre playlists basada en contenido y usuarios"""
    playlist_a_id = models.IntegerField()
    playlist_b_id = models.IntegerField()
    similitud_contenido = models.FloatField(default=0.0)  # Basada en canciones comunes
    similitud_usuarios = models.FloatField(default=0.0)   # Basada en usuarios que las siguen
    similitud_total = models.FloatField(default=0.0)      # Puntuación combinada
    canciones_comunes = models.IntegerField(default=0)
    usuarios_comunes = models.IntegerField(default=0)
    calculada_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'similitud_playlists'
        unique_together = ('playlist_a_id', 'playlist_b_id')
        ordering = ['-similitud_total']

    def __str__(self):
        return f"Similitud Playlists {self.playlist_a_id}-{self.playlist_b_id}: {self.similitud_total}"

class RecomendacionPlaylist(models.Model):
    """Recomendaciones de playlists para usuarios"""
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
        return f"User {self.usuario_id}: Playlist {self.playlist_recomendada_id} ({self.razon_recomendacion})"

class CategoriasPlaylist(models.Model):
    """Categorías y etiquetas para clasificar playlists"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    color_hex = models.CharField(max_length=7, default='#000000')  # Color para UI
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
        return self.nombre

class PlaylistCategoria(models.Model):
    """Relación many-to-many entre playlists y categorías"""
    playlist_id = models.IntegerField()
    categoria = models.ForeignKey(CategoriasPlaylist, on_delete=models.CASCADE)
    relevancia = models.FloatField(default=1.0)  # Qué tan relevante es esta categoría para la playlist
    asignada_automaticamente = models.BooleanField(default=False)
    asignada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'playlist_categorias'
        unique_together = ('playlist_id', 'categoria')

    def __str__(self):
        return f"Playlist {self.playlist_id} - {self.categoria.nombre}"
