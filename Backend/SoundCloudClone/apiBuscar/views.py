from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apiCanciones.models import Cancion
from apiPlaylists.models import Playlist
from .serializers import CancionSerializer, PlaylistSerializer

class BuscarView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({"error": "Debes proporcionar un parámetro de búsqueda (?q=...)"},
                            status=status.HTTP_400_BAD_REQUEST)

        canciones = Cancion.objects.filter(titulo__icontains=query)
        playlists = Playlist.objects.filter(nombre__icontains=query)

        canciones_serializadas = CancionSerializer(canciones, many=True).data
        playlists_serializadas = PlaylistSerializer(playlists, many=True).data

        return Response({
            "canciones": canciones_serializadas,
            "playlists": playlists_serializadas
        })
