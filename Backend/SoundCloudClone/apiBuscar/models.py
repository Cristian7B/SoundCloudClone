from django.db import models

class IndicesBusqueda(models.Model):
    """Modelo para cachear y optimizar búsquedas frecuentes"""
    termino_busqueda = models.CharField(max_length=255, unique=True)
    resultados_canciones = models.JSONField(default=list)
    resultados_playlists = models.JSONField(default=list)
    resultados_usuarios = models.JSONField(default=list)
    frecuencia_busqueda = models.IntegerField(default=1)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'indices_busqueda'
        ordering = ['-frecuencia_busqueda', '-ultima_actualizacion']

    def __str__(self):
        return f"Búsqueda: {self.termino_busqueda} (freq: {self.frecuencia_busqueda})"

class HistorialBusqueda(models.Model):
    """Historial de búsquedas por usuario"""
    usuario_id = models.IntegerField()  # Referencia al usuario por ID
    termino_busqueda = models.CharField(max_length=255)
    resultados_encontrados = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historial_busqueda'
        ordering = ['-created_at']

    def __str__(self):
        return f"User {self.usuario_id}: {self.termino_busqueda}"

class SugerenciasBusqueda(models.Model):
    """Sugerencias de búsqueda populares"""
    termino = models.CharField(max_length=255, unique=True)
    categoria = models.CharField(max_length=50, choices=[
        ('cancion', 'Canción'),
        ('playlist', 'Playlist'),
        ('usuario', 'Usuario'),
        ('genero', 'Género'),
        ('album', 'Album'),
    ])
    popularidad = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sugerencias_busqueda'
        ordering = ['-popularidad']

    def __str__(self):
        return f"{self.termino} ({self.categoria})"
