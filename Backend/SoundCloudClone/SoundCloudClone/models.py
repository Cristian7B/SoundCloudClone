from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Cancion(models.Model):
    titulo = models.CharField(max_length=255)
    archivo_url = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='canciones')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Playlist(models.Model):
    titulo = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class PlaylistCancion(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playlist', 'cancion')

    def __str__(self):
        return f'{self.playlist.titulo} - {self.cancion.titulo}'
