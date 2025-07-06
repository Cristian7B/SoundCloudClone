import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apiPlaylists.models import Playlist
from apiPlaylists.serializers import PlaylistSerializer  # Reutilizamos el serializer

class SugerenciaPlaylistsView(APIView):
    def get(self, request):
        todas_playlists = list(Playlist.objects.all())

        if not todas_playlists:
            return Response({"mensaje": "No hay playlists disponibles."}, status=status.HTTP_404_NOT_FOUND)

        seleccionadas = random.sample(todas_playlists, min(3, len(todas_playlists)))
        serializadas = PlaylistSerializer(seleccionadas, many=True)

        return Response(serializadas.data, status=status.HTTP_200_OK)
