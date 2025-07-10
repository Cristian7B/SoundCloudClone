from django.db import models

class PreferenciasUsuario(models.Model):
    """Preferencias y patrones de comportamiento del usuario"""
    usuario_id = models.IntegerField(unique=True)  # Referencia al usuario por ID
    generos_favoritos = models.JSONField(default=list)  # Lista de géneros
    artistas_seguidos = models.JSONField(default=list)  # Lista de IDs de artistas
    total_reproducciones = models.IntegerField(default=0)
    canciones_gustadas = models.IntegerField(default=0)
    playlists_creadas = models.IntegerField(default=0)
    ultima_actividad = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'preferencias_usuario'

    def __str__(self):
        return f"Preferencias User {self.usuario_id}"

class HistorialReproduccion(models.Model):
    """Historial de reproducciones para generar recomendaciones"""
    usuario_id = models.IntegerField()  # Referencia al usuario por ID
    cancion_id = models.IntegerField()  # Referencia a la canción por ID
    duracion_reproducida = models.DurationField()  # Tiempo que escuchó
    porcentaje_escuchado = models.FloatField()  # % de la canción escuchada
    dispositivo = models.CharField(max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    hora_del_dia = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_reproducciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"User {self.usuario_id} - Song {self.cancion_id} ({self.porcentaje_escuchado}%)"

class SimilitudCanciones(models.Model):
    """Matriz de similitud entre canciones para recomendaciones"""
    cancion_a_id = models.IntegerField()
    cancion_b_id = models.IntegerField()
    puntuacion_similitud = models.FloatField()  # 0.0 a 1.0
    factores_similitud = models.JSONField(default=dict)  # géneros, artista, etc.
    calculada_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'similitud_canciones'
        unique_together = ('cancion_a_id', 'cancion_b_id')
        ordering = ['-puntuacion_similitud']

    def __str__(self):
        return f"Similitud {self.cancion_a_id}-{self.cancion_b_id}: {self.puntuacion_similitud}"

class RecomendacionGenerada(models.Model):
    """Cache de recomendaciones generadas para usuarios"""
    usuario_id = models.IntegerField()
    canciones_recomendadas = models.JSONField(default=list)  # Lista de IDs de canciones
    algoritmo_usado = models.CharField(max_length=50)  # collaborative, content-based, etc.
    puntuacion_confianza = models.FloatField()
    valida_hasta = models.DateTimeField()
    generada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recomendaciones_generadas'
        ordering = ['-generada_en']

    def __str__(self):
        return f"Recomendaciones User {self.usuario_id} ({self.algoritmo_usado})"

class FeedbackRecomendacion(models.Model):
    """Feedback del usuario sobre las recomendaciones para mejorar el algoritmo"""
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
        return f"User {self.usuario_id}: {self.accion} song {self.cancion_recomendada_id}"
