"""
URL configuration for playlist recommendation API.

This module defines the URL patterns for the playlist recommendation system,
providing endpoints for playlist discovery and curated suggestions.

URL Patterns:
    '' (root): Main playlist recommendation endpoint

API Endpoints:
    GET /api/sugerencias-playlists/ - Get curated playlist recommendations

Features:
    - Random playlist discovery for content exploration
    - Future support for ML-based personalized recommendations
    - Category and mood-based suggestions (planned)
    - Public access for all users including guests
    - Scalable architecture for advanced recommendation algorithms

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.urls import path
from .views import SugerenciaPlaylistsView

urlpatterns = [
    # Playlist Recommendations Endpoint
    # GET /api/sugerencias-playlists/ - Get playlist recommendations
    path('', SugerenciaPlaylistsView.as_view(), name='sugerencias-playlists'),
]
