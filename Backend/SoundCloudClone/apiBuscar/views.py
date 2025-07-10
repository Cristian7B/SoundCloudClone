from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apiPersistencia.models import Cancion, Playlist
from .models import IndicesBusqueda, HistorialBusqueda, SugerenciasBusqueda
from .serializers import CancionSerializer, PlaylistSerializer

class BuscarView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        usuario_id = getattr(request.user, 'user_id', None) if request.user.is_authenticated else None

        if not query:
            return Response({"error": "Debes proporcionar un parámetro de búsqueda (?q=...)"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Buscar canciones
        canciones = Cancion.objects.filter(titulo__icontains=query)[:20]
        
        # Buscar playlists
        playlists = Playlist.objects.filter(titulo__icontains=query, es_publica=True)[:20]

        # Serializar resultados
        canciones_serializadas = CancionSerializer(canciones, many=True).data
        playlists_serializadas = PlaylistSerializer(playlists, many=True).data

        # Guardar en historial si el usuario está autenticado
        if usuario_id:
            HistorialBusqueda.objects.create(
                usuario_id=usuario_id,
                termino_busqueda=query,
                resultados_encontrados=len(canciones) + len(playlists)
            )

        # Actualizar o crear índice de búsqueda
        indice, created = IndicesBusqueda.objects.get_or_create(
            termino_busqueda=query.lower(),
            defaults={
                'resultados_canciones': [c['cancion_id'] for c in canciones_serializadas],
                'resultados_playlists': [p['playlist_id'] for p in playlists_serializadas],
            }
        )
        if not created:
            indice.frecuencia_busqueda += 1
            indice.save()

        return Response({
            "query": query,
            "canciones": canciones_serializadas,
            "playlists": playlists_serializadas,
            "total_resultados": len(canciones) + len(playlists)
        }, status=status.HTTP_200_OK)

class SugerenciasView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Obtener sugerencias de búsqueda populares"""
        sugerencias = SugerenciasBusqueda.objects.filter(activo=True)[:10]
        return Response({
            "sugerencias": [{"termino": s.termino, "categoria": s.categoria} for s in sugerencias]
        }, status=status.HTTP_200_OK)
