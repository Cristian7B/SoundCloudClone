from django.db import models
from django.conf import settings

class Album(models.Model):
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
