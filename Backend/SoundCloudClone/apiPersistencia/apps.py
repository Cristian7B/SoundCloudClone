"""
Django application configuration for the music content persistence module.

This module configures the apiPersistencia Django application, which handles
the core music content management functionality including songs, playlists,
albums, and user interactions within the SoundCloud clone.

Classes:
    ApipersistenciaConfig: Main application configuration class

Application Features:
    - Music content CRUD operations (songs, playlists, albums)
    - User interaction tracking (likes, reposts, follows)
    - Playlist-song relationship management
    - Content search and filtering
    - User-generated content organization
    - Statistics and analytics for content

Database Models:
    - Cancion: Individual songs and tracks
    - Playlist: User-created playlists
    - Album: Music album collections
    - PlaylistCancion: Many-to-many relationship for playlist songs
    - Interaccion: User engagement tracking

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.apps import AppConfig


class ApipersistenciaConfig(AppConfig):
    """
    Configuration class for the apiPersistencia Django application.
    
    Defines the application settings and metadata for the music content
    persistence module, including field type defaults and application name.
    
    Attributes:
        default_auto_field: Specifies the default primary key field type
                           for models in this application
        name: The fully qualified name of the application module
    
    Purpose:
        - Configures database field defaults for optimal performance
        - Enables Django's application registry to properly manage the module
        - Provides namespace isolation for the persistence functionality
        - Supports Django's app-level configuration and initialization
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apiPersistencia'
