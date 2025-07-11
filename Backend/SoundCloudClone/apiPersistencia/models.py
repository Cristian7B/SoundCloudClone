from django.db import models
from django.conf import settings

class Album(models.Model):
    """
        Modelo que representa un álbum musical en el sistema.

        Atributos:
            album_id (AutoField): Identificador único del álbum
            titulo (CharField): Nombre del álbum
            descripcion (TextField): Descripción detallada del álbum (opcional)
            imagen_url (URLField): URL de la imagen de portada del álbum (opcional)
            usuario_id (IntegerField): ID del usuario que creó el álbum
            created_at (DateTimeField): Fecha y hora de creación
            updated_at (DateTimeField): Fecha y hora de última actualización
    """
    album_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    usuario_id = models.IntegerField()  # Referencia al usuario por ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'albums'
        ordering = ['-created_at']

class Cancion(models.Model):
    """
        Modelo que representa una canción en el sistema.

        Atributos:
            cancion_id (AutoField): Identificador único de la canción
            titulo (CharField): Nombre de la canción
            descripcion (TextField): Descripción de la canción (opcional)
            archivo_url (URLField): URL del archivo de audio
            imagen_url (URLField): URL de la imagen de portada (opcional)
            duracion (DurationField): Duración de la canción
            genero (CharField): Género musical de la canción
            usuario_id (IntegerField): ID del usuario que subió la canción
            album (ForeignKey): Referencia al álbum al que pertenece
            reproducciones (IntegerField): Contador de reproducciones
            likes_count (IntegerField): Contador de "me gusta"
            reposts_count (IntegerField): Contador de reposteos
    """
    cancion_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    archivo_url = models.URLField()
    imagen_url = models.URLField(blank=True, null=True)
    duracion = models.DurationField(null=True, blank=True)
    genero = models.CharField(max_length=100, blank=True, null=True)
    usuario_id = models.IntegerField()  # Referencia al usuario por ID
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='canciones')
    reproducciones = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    reposts_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'canciones'
        ordering = ['-created_at']

class Playlist(models.Model):
    """
        Modelo que representa una lista de reproducción.

        Atributos:
            playlist_id (AutoField): Identificador único de la playlist
            titulo (CharField): Nombre de la playlist
            descripcion (TextField): Descripción de la playlist (opcional)
            imagen_url (URLField): URL de la imagen de portada (opcional)
            usuario_id (IntegerField): ID del usuario creador
            es_publica (BooleanField): Indica si la playlist es pública
    """
    playlist_id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    usuario_id = models.IntegerField()  # Referencia al usuario por ID
    es_publica = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'playlists'
        ordering = ['-created_at']

class PlaylistCancion(models.Model):
    """
        Modelo que representa la relación entre Playlist y Cancion.
        Permite ordenar las canciones dentro de una playlist.

        Atributos:
            playlist (ForeignKey): Referencia a la playlist
            cancion (ForeignKey): Referencia a la canción
            orden (IntegerField): Posición de la canción en la playlist
            added_at (DateTimeField): Fecha y hora de agregado
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
        return f'{self.playlist.titulo} - {self.cancion.titulo}'

class Interaccion(models.Model):
    """
        Modelo que representa las interacciones de usuarios con canciones, playlists y otros usuarios.

        Atributos:
            usuario_id (IntegerField): ID del usuario que realiza la interacción
            cancion (ForeignKey): Referencia a la canción (opcional)
            playlist (ForeignKey): Referencia a la playlist (opcional)
            usuario_objetivo_id (IntegerField): ID del usuario objetivo (para follows)
            tipo (CharField): Tipo de interacción (like, repost, follow)
            created_at (DateTimeField): Fecha y hora de la interacción

        Notas:
            - Solo uno de los campos cancion, playlist o usuario_objetivo_id debe estar presente
            - Las combinaciones únicas evitan interacciones duplicadas
    """
    TIPO_CHOICES = [
        ('like', 'Like'),
        ('repost', 'Repost'),
        ('follow', 'Follow'),
    ]
    
    usuario_id = models.IntegerField()  # Referencia al usuario por ID
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, null=True, blank=True, related_name='interacciones')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, blank=True, related_name='interacciones')
    usuario_objetivo_id = models.IntegerField(null=True, blank=True)  # Para follows
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
        if self.cancion:
            return f'User {self.usuario_id} {self.tipo} {self.cancion.titulo}'
        elif self.playlist:
            return f'User {self.usuario_id} {self.tipo} {self.playlist.titulo}'
        else:
            return f'User {self.usuario_id} {self.tipo} User {self.usuario_objetivo_id}'
