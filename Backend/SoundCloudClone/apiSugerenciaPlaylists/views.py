import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apiPersistencia.models import Playlist
from apiBuscar.serializers import PlaylistSerializer

class SugerenciaPlaylistsView(APIView):
    """
    Vista para sugerir playlists aleatorias.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        todas_playlists = list(Playlist.objects.filter(es_publica=True))

        if not todas_playlists:
            return Response({
                "mensaje": "No hay playlists disponibles."
            }, status=status.HTTP_404_NOT_FOUND)

        # Tomar 5 playlists aleatorias
        cantidad = min(5, len(todas_playlists))
        seleccionadas = random.sample(todas_playlists, cantidad)
        serializadas = PlaylistSerializer(seleccionadas, many=True)

        return Response({
            "mensaje": f"Se encontraron {cantidad} playlists sugeridas",
            "playlists": serializadas.data
        }, status=status.HTTP_200_OK)
