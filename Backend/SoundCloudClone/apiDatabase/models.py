from django.db import models

class EstadisticasGenerales(models.Model):
    """Estadísticas generales del sistema"""
    total_usuarios = models.IntegerField(default=0)
    total_canciones = models.IntegerField(default=0)
    total_playlists = models.IntegerField(default=0)
    total_reproducciones_hoy = models.IntegerField(default=0)
    total_reproducciones_mes = models.IntegerField(default=0)
    usuarios_activos_hoy = models.IntegerField(default=0)
    usuarios_activos_mes = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estadisticas_generales'

    def __str__(self):
        return f"Stats {self.fecha_actualizacion.date()}"

class RegistroActividad(models.Model):
    """Log de actividades importantes del sistema"""
    usuario_id = models.IntegerField(null=True, blank=True)
    accion = models.CharField(max_length=50, choices=[
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('upload_song', 'Subir Canción'),
        ('create_playlist', 'Crear Playlist'),
        ('delete_song', 'Eliminar Canción'),
        ('delete_playlist', 'Eliminar Playlist'),
        ('follow_user', 'Seguir Usuario'),
        ('unfollow_user', 'Dejar de Seguir'),
    ])
    detalles = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registro_actividades'
        ordering = ['-timestamp']

    def __str__(self):
        if self.usuario_id:
            return f"User {self.usuario_id}: {self.accion}"
        return f"System: {self.accion}"

class ConfiguracionSistema(models.Model):
    """Configuraciones dinámicas del sistema"""
    clave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    tipo_dato = models.CharField(max_length=20, choices=[
        ('string', 'Texto'),
        ('integer', 'Número Entero'),
        ('float', 'Número Decimal'),
        ('boolean', 'Verdadero/Falso'),
        ('json', 'JSON'),
    ], default='string')
    modificable_por_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'configuracion_sistema'
        ordering = ['clave']

    def __str__(self):
        return f"{self.clave}: {self.valor}"