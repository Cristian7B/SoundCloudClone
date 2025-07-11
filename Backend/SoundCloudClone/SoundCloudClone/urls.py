"""
Main URL configuration for SoundCloudClone project.

This module defines the root URL routing for the entire SoundCloud clone application.
It organizes API endpoints into logical groups by functionality and delegates specific
URL patterns to individual application modules for better maintainability.

URL Structure:
    /admin/ - Django admin interface for development and management
    /api/auth/ - User authentication and profile management endpoints
    /api/contenido/ - Music content management (songs, playlists, albums)
    /api/buscar/ - Search functionality for content discovery
    /api/sugerencias-canciones/ - Song recommendation system endpoints
    /api/sugerencias-playlists/ - Playlist recommendation system endpoints
    /api/database/ - Database management and utility endpoints

API Design Principles:
    - RESTful endpoint structure with clear resource hierarchies
    - Logical grouping by functionality for easy navigation
    - Consistent naming conventions across all modules
    - Scalable architecture supporting feature additions

Example Endpoints:
    POST /api/auth/registro/ - User registration
    GET /api/contenido/canciones/ - List all songs
    GET /api/buscar/canciones/?q=search_term - Search songs
    POST /api/contenido/playlists/{id}/agregar-cancion/ - Add song to playlist

Security Features:
    - JWT-based authentication for protected endpoints
    - CORS configuration for frontend integration
    - Admin interface restricted to superusers
    - Permission-based access control per endpoint

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Interface
    # Provides web-based administration for models and user management
    path('admin/', admin.site.urls),
    
    # Authentication API
    # Handles user registration, login, profile management, and email notifications
    path('api/auth/', include('apiAutenticacion.urls')),
    
    # Content Management API
    # Manages songs, playlists, albums, and user interactions (likes, reposts, follows)
    path('api/contenido/', include('apiPersistencia.urls')),
    
    # Search API
    # Provides real-time search functionality for songs, playlists, and users
    path('api/buscar/', include('apiBuscar.urls')),
    
    # Song Recommendation API
    # Delivers personalized song recommendations based on user preferences
    path('api/sugerencias-canciones/', include('apiSugerenciaCanciones.urls')),
    
    # Playlist Recommendation API
    # Provides curated playlist suggestions and discovery features
    path('api/sugerencias-playlists/', include('apiSugerenciaPlaylists.urls')),
    
    # Database Utility API
    # Handles database operations, analytics, and administrative functions
    path('api/database/', include('apiDatabase.urls')),
]