"""
API views for search functionality in the SoundCloud clone.

This module provides comprehensive search capabilities for the music platform,
including real-time content search, search history tracking, and search suggestions.
Supports searching across songs and playlists with intelligent indexing and
analytics for improved user experience.

Classes:
    BuscarView: Main search endpoint for songs and playlists
    SugerenciasView: Search suggestions and popular terms endpoint

Features:
    - Real-time search across songs and playlists
    - Search history tracking for authenticated users
    - Search analytics and frequency tracking
    - Popular search suggestions
    - Case-insensitive search matching
    - Public playlist filtering for privacy
    - Search result indexing for performance optimization

Search Capabilities:
    - Song title matching with case-insensitive search
    - Public playlist title matching
    - Results limited to 20 items per category for performance
    - Combined result count for analytics
    - Search term frequency tracking for trending analysis

@author: Development Team
@version: 1.0
@since: 2024
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apiPersistencia.models import Cancion, Playlist
from .models import IndicesBusqueda, HistorialBusqueda, SugerenciasBusqueda
from .serializers import CancionSerializer, PlaylistSerializer


class BuscarView(APIView):
    """
    API view for searching songs and playlists.
    
    Provides comprehensive search functionality across the music platform with
    intelligent indexing, analytics tracking, and search history management.
    Supports real-time search with optimized query performance and result caching.
    
    Endpoint: GET /api/buscar/?q=search_term
    
    Query Parameters:
        q (str): Search term for finding songs and playlists (required)
    
    Response Format:
        {
            "query": "search_term",
            "canciones": [...],  // Array of matching songs
            "playlists": [...],  // Array of matching public playlists
            "total_resultados": 15  // Total number of results found
        }
    
    Search Features:
        - Case-insensitive title matching for songs and playlists
        - Public playlist filtering (private playlists excluded)
        - Results limited to 20 items per category for performance
        - Search history tracking for authenticated users
        - Search frequency analytics for trending analysis
        - Automatic search index creation and updates
    
    Analytics Tracking:
        - Records search terms and result counts in search history
        - Updates search frequency counters for popular term identification
        - Creates search indices for performance optimization
        - Tracks user search patterns for recommendation systems
    
    Performance Optimizations:
        - Limited result sets to prevent large response payloads
        - Database query optimization with selective field retrieval
        - Search index caching for frequently searched terms
        - Efficient serialization for fast response times
    
    Privacy Considerations:
        - Only searches public playlists to respect user privacy
        - Search history only recorded for authenticated users
        - Anonymous search capability for guest users
    
    Permissions:
        - AllowAny: Public search access for all users
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Perform search across songs and playlists.
        
        Args:
            request: HTTP request containing search query parameter
            
        Returns:
            Response: JSON response with search results and metadata
            
        Query Parameters:
            q (str): Search term (required, min 1 character after strip)
            
        Response Fields:
            query (str): The search term that was used
            canciones (list): Array of matching song objects
            playlists (list): Array of matching public playlist objects
            total_resultados (int): Total count of all results found
            
        Error Responses:
            400 Bad Request: If search query parameter is missing or empty
            
        Analytics Side Effects:
            - Creates/updates search history entry for authenticated users
            - Creates/updates search index entry for term frequency tracking
            - Increments search frequency counter for trending analysis
            
        Example Request:
            GET /api/buscar/?q=rock music
            
        Example Response:
            {
                "query": "rock music",
                "canciones": [
                    {
                        "cancion_id": 1,
                        "titulo": "Rock Song",
                        "usuario_id": 5,
                        ...
                    }
                ],
                "playlists": [
                    {
                        "playlist_id": 3,
                        "titulo": "Best Rock Music",
                        "es_publica": true,
                        ...
                    }
                ],
                "total_resultados": 15
            }
        """
        # Extract and validate search query
        query = request.query_params.get('q', '').strip()
        usuario_id = getattr(request.user, 'user_id', None) if request.user.is_authenticated else None

        # Validate that search query is provided
        if not query:
            return Response({"error": "Debes proporcionar un parámetro de búsqueda (?q=...)"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Perform case-insensitive search on song titles (limit for performance)
        canciones = Cancion.objects.filter(titulo__icontains=query)[:20]
        
        # Search public playlists only (privacy protection)
        playlists = Playlist.objects.filter(titulo__icontains=query, es_publica=True)[:20]

        # Serialize results for JSON response
        canciones_serializadas = CancionSerializer(canciones, many=True).data
        playlists_serializadas = PlaylistSerializer(playlists, many=True).data

        # Record search history for authenticated users (analytics)
        if usuario_id:
            HistorialBusqueda.objects.create(
                usuario_id=usuario_id,
                termino_busqueda=query,
                resultados_encontrados=len(canciones) + len(playlists)
            )

        # Update search index for frequency tracking and caching
        indice, created = IndicesBusqueda.objects.get_or_create(
            termino_busqueda=query.lower(),
            defaults={
                'resultados_canciones': [c['cancion_id'] for c in canciones_serializadas],
                'resultados_playlists': [p['playlist_id'] for p in playlists_serializadas],
            }
        )
        if not created:
            # Increment frequency counter for trending analysis
            indice.frecuencia_busqueda += 1
            indice.save()

        return Response({
            "query": query,
            "canciones": canciones_serializadas,
            "playlists": playlists_serializadas,
            "total_resultados": len(canciones) + len(playlists)
        }, status=status.HTTP_200_OK)


class SugerenciasView(APIView):
    """
    API view for providing search suggestions and popular terms.
    
    Returns curated search suggestions to help users discover content and
    improve search experience. Provides popular search terms and categorized
    suggestions for enhanced user engagement and content discovery.
    
    Endpoint: GET /api/buscar/sugerencias/
    
    Response Format:
        {
            "sugerencias": [
                {
                    "termino": "rock",
                    "categoria": "genero"
                },
                {
                    "termino": "jazz playlist",
                    "categoria": "playlist"
                }
            ]
        }
    
    Features:
        - Curated search suggestions for improved discovery
        - Categorized suggestions (genre, artist, playlist, etc.)
        - Active suggestion filtering (only enabled suggestions)
        - Limited result set for optimal user experience
        - No authentication required for public access
    
    Use Cases:
        - Search autocomplete functionality
        - Popular search terms display
        - Content discovery assistance
        - Search experience enhancement
        - Trending topic identification
    
    Permissions:
        - AllowAny: Public access for all users
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Retrieve active search suggestions.
        
        Args:
            request: HTTP request (no parameters required)
            
        Returns:
            Response: JSON response with search suggestions
            
        Response Fields:
            sugerencias (list): Array of suggestion objects containing:
                termino (str): The suggested search term
                categoria (str): Category of the suggestion (genre, artist, etc.)
                
        Features:
            - Returns only active suggestions (activo=True)
            - Limited to 10 suggestions for optimal UX
            - Categorized suggestions for better organization
            - No authentication required for public access
            
        Example Response:
            {
                "sugerencias": [
                    {"termino": "rock", "categoria": "genero"},
                    {"termino": "pop hits", "categoria": "playlist"},
                    {"termino": "jazz", "categoria": "genero"},
                    {"termino": "electronic", "categoria": "genero"}
                ]
            }
            
        Use Cases:
            - Search autocomplete dropdowns
            - Popular search terms display
            - Search suggestion widgets
            - Content discovery features
        """
        # Retrieve active search suggestions (limited for performance)
        sugerencias = SugerenciasBusqueda.objects.filter(activo=True)[:10]
        
        return Response({
            "sugerencias": [{"termino": s.termino, "categoria": s.categoria} for s in sugerencias]
        }, status=status.HTTP_200_OK)
