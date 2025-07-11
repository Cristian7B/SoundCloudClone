"""
Database models for system administration and analytics.

This module defines models for system-wide statistics, activity logging,
and dynamic configuration management. These models support administrative
functions, performance monitoring, and system analytics for the SoundCloud clone.

Classes:
    EstadisticasGenerales: System-wide statistics and metrics
    RegistroActividad: Activity logging for user and system actions
    ConfiguracionSistema: Dynamic system configuration management

Features:
    - Real-time system statistics tracking
    - Comprehensive activity logging for audit trails
    - Dynamic configuration without code changes
    - Performance monitoring and analytics
    - User behavior tracking for insights

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.db import models


class EstadisticasGenerales(models.Model):
    """
    Model for tracking system-wide statistics and performance metrics.
    
    Stores aggregated data about platform usage including user counts,
    content statistics, and activity metrics. Updated regularly to provide
    real-time insights into platform health and growth.
    
    Attributes:
        total_usuarios: Total number of registered users
        total_canciones: Total number of uploaded songs
        total_playlists: Total number of created playlists
        total_reproducciones_hoy: Daily play count
        total_reproducciones_mes: Monthly play count
        usuarios_activos_hoy: Daily active users
        usuarios_activos_mes: Monthly active users
        fecha_actualizacion: Last update timestamp
    
    Usage:
        - Dashboard analytics display
        - Performance monitoring
        - Growth tracking
        - Administrative reporting
    
    Database Table: estadisticas_generales
    """
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
    """
    Model for logging user and system activities for audit and analytics.
    
    Tracks important actions performed by users and system processes,
    providing a comprehensive audit trail for security, debugging, and
    user behavior analysis.
    
    Attributes:
        usuario_id: ID of the user who performed the action (null for system actions)
        accion: Type of action performed (login, upload, create, etc.)
        detalles: Additional details about the action in JSON format
        ip_address: IP address from which the action was performed
        user_agent: Browser/client information
        timestamp: When the action occurred
    
    Action Types:
        - login/logout: Authentication events
        - upload_song: Song upload activities
        - create_playlist: Playlist creation
        - delete_song/delete_playlist: Content deletion
        - follow_user/unfollow_user: Social interactions
    
    Usage:
        - Security auditing
        - User behavior analysis
        - Debugging and troubleshooting
        - Analytics and reporting
    
    Database Table: registro_actividades
    """
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
    """
    Model for dynamic system configuration management.
    
    Allows runtime configuration changes without code modifications,
    supporting flexible system behavior and feature toggles.
    
    Attributes:
        clave: Unique configuration key identifier
        valor: Configuration value (stored as text)
        descripcion: Human-readable description of the configuration
        tipo_dato: Data type of the value (string, integer, float, boolean, json)
        modificable_por_admin: Whether admins can modify this configuration
        created_at: When the configuration was created
        updated_at: When the configuration was last modified
    
    Data Types:
        - string: Text values
        - integer: Whole numbers
        - float: Decimal numbers
        - boolean: True/False values
        - json: Complex data structures
    
    Usage:
        - Feature flags and toggles
        - System limits and thresholds
        - API rate limiting settings
        - Email configuration
        - Third-party service settings
    
    Database Table: configuracion_sistema
    """
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