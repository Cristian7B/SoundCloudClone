from django.db import models, IntegrityError

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstratBaseUser

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from SoundCloudClone.models import *

class AppUserManager(BaseUserManager):
          def create_user(self, email, username, password = None):
                    if not email:
                              raise ValueError('The Email Field must be set')
                    if not password: 
                              raise ValueError('The password must be set')
                    
                    email = self.normalize_email(email)

                    try:
                              validate_email(email)
                    except ValidationError:
                              raise ValueError('The email is not valid')

                    user = self.model(email = email, username = username)
                    user.set_password(password)

                    try:
                              user.save()
                    except IntegrityError:
                              raise ValueError('A user with this email already exists')
                    
                    return user

class appUser(AbstratBaseUser):
          user_id = models.AutoField(primary_key=True)
          nombre = models.CharField(max_length=100)
          email = models.EmailField(unique=True)
          password_hash = models.CharField(max_length=255)
          created_at = models.DateTimeField(auto_now_add=True)

          def __str__(self):
                    return self.nombre

          class Meta:
                    db_table = 'Usuarios'

class Cancion(modles.Model):
          cancion_id = models.AutoField(primary_key=True)
          titulo = models.CharField(max_length=255)
          archivo_url = models.TextField()
          usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='canciones')
          created_at = models.DateTimeField(auto_now_add=True)
          cancion_foranea= models.ForeignKey(
                    CancionPlaylist,
                    on_delete=models.CASCADE,
                    related_name='cancion'
          )

          def __str__(self):
                    return self.titulo
          
          class Meta:
                    db_table = 'Canciones'

class Playlist(models.Model):
          playlist_id = models.AutoField(primary_key=True)
          titulo = models.CharField(max_length=255)
          usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='playlists')
          created_at = models.DateTimeField(auto_now_add=True)
          playlist_foranea = models.ForeignKey(
                    CancionPlaylist,
                    on_delete=models.CASCADE,
                    related_name = 'playlist'
          )

          def __str__(self):
                    return self.titulo

          class Meta:
                    db_table = 'Playlists'

class CancionPlaylist(models.Model):
          nombre  = models.CharField(max_length=50)