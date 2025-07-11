"""
URL configuration for song recommendation API.

This module defines the URL patterns for the song recommendation system,
providing endpoints for music discovery and personalized song suggestions.

URL Patterns:
    '' (root): Main song recommendation endpoint

API Endpoints:
    GET /api/sugerencias-canciones/ - Get personalized song recommendations

Features:
    - Random song discovery for content exploration
    - Future support for ML-based personalized recommendations
    - Public access for all users including guests
    - Scalable architecture for algorithm improvements

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.urls import path
from .views import SugerenciaCancionesView

urlpatterns = [
    # Song Recommendations Endpoint
    # GET /api/sugerencias-canciones/ - Get song recommendations
    path('', SugerenciaCancionesView.as_view(), name='sugerencias-canciones'),
]
