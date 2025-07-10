from rest_framework import serializers
from apiCanciones.models import Cancion
from apiPlaylists.models import Playlist

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = ['id', 'titulo', 'artista']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'nombre', 'descripcion']
