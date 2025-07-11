"""
URL configuration for search functionality API.

This module defines URL patterns for the search system, providing endpoints
for real-time content search and search suggestions within the SoundCloud clone.

URL Patterns:
    '' (root): Main search endpoint for content discovery
    sugerencias/: Search suggestions and trending terms

API Endpoints:
    GET /api/buscar/?q=search_term - Search songs and playlists
    GET /api/buscar/sugerencias/ - Get search suggestions and trending terms

Features:
    - Real-time search across songs and playlists
    - Search history tracking for authenticated users
    - Search suggestion system
    - Performance-optimized search queries
    - Public content filtering for privacy

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.urls import path
from .views import BuscarView, SugerenciasView

urlpatterns = [
    # Main Search Endpoint
    # GET /api/buscar/?q=search_term - Search for songs and playlists
    path('', BuscarView.as_view(), name='buscar'),
    
    # Search Suggestions Endpoint
    # GET /api/buscar/sugerencias/ - Get search suggestions and popular terms
    path('sugerencias/', SugerenciasView.as_view(), name='sugerencias_busqueda'),
]
