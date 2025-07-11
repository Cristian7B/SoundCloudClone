"""
API views for song recommendation and discovery services.

This module provides the core song recommendation functionality for the SoundCloud clone,
delivering personalized song suggestions to enhance user music discovery experience.
Currently implements random sampling with plans for sophisticated ML-based algorithms.

Classes:
    SugerenciaCancionesView: Main API view for song recommendations

Features:
    - Random song discovery for content exploration
    - Scalable architecture for future ML integration
    - Fast response times with limited result sets
    - Public access for all users including guests

@author: Development Team
@version: 1.0
@since: 2024
"""

import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apiPersistencia.models import Cancion
from apiBuscar.serializers import CancionSerializer


class SugerenciaCancionesView(APIView):
    """
    API view for providing song recommendations and music discovery.
    
    Delivers curated song suggestions to users for content discovery and
    exploration. Currently implements random sampling of available songs
    with plans for sophisticated recommendation algorithms based on user
    listening history, preferences, and collaborative filtering.
    
    Endpoint: GET /api/sugerencias-canciones/
    
    Response Format:
        {
            "mensaje": "Se encontraron 5 canciones sugeridas",
            "canciones": [
                {
                    "cancion_id": 1,
                    "titulo": "Song Title",
                    "descripcion": "Song description",
                    "archivo_url": "https://example.com/song.mp3",
                    "imagen_url": "https://example.com/cover.jpg",
                    "usuario_id": 123,
                    "genero": "Pop",
                    "duracion": "00:03:45",
                    "reproducciones": 1000,
                    "likes_count": 50,
                    "created_at": "2024-01-01T00:00:00Z"
                },
                ...
            ]
        }
    
    Current Algorithm:
        - Randomly samples up to 5 songs from all available tracks
        - Ensures variety and discovery of different content
        - No user personalization (suitable for anonymous users)
    
    Planned Enhancements:
        - User-based collaborative filtering
        - Content-based recommendations using audio features
        - Trending song identification
        - Genre and mood-based suggestions
        - Social influence from followed users' activity
        - Machine learning models for personalization
        - Listening history analysis
        - Context-aware recommendations (time, location, activity)
    
    Performance Considerations:
        - Limited result set (5 songs) for fast response times
        - Efficient random sampling for large music catalogs
        - Database query optimization for song retrieval
        - Full song serialization for immediate playback
    
    Permissions:
        - AllowAny: Public access for all users including guests
    
    Error Handling:
        - Graceful handling of empty music catalog
        - Clear error messages for no available content
        - Fallback responses for edge cases
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        todas_canciones = list(Cancion.objects.all())

        if len(todas_canciones) == 0:
            return Response({
                "mensaje": "No hay canciones disponibles."
            }, status=status.HTTP_404_NOT_FOUND)

        # Tomar 5 canciones aleatorias
        cantidad = min(5, len(todas_canciones))
        canciones_aleatorias = random.sample(todas_canciones, cantidad)
        canciones_serializadas = CancionSerializer(canciones_aleatorias, many=True)

        return Response({
            "mensaje": f"Se encontraron {cantidad} canciones sugeridas",
            "canciones": canciones_serializadas.data
        }, status=status.HTTP_200_OK)
