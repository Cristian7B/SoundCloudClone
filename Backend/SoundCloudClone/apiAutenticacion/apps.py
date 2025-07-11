"""
Django application configuration for the user authentication module.

This module configures the apiAutenticacion Django application, which handles
all user authentication, registration, and profile management functionality
for the SoundCloud clone platform.

Classes:
    ApiautenticacionConfig: Main application configuration class

Application Features:
    - User registration with email verification
    - JWT-based authentication system
    - User profile management and updates
    - Password reset and recovery
    - Email notification services
    - Session management and logout
    - Public user information access

Security Features:
    - Secure password hashing
    - JWT token generation and validation
    - Email-based authentication
    - Token blacklisting for logout
    - Protected profile endpoints

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.apps import AppConfig


class ApiautenticacionConfig(AppConfig):
    """
    Configuration class for the apiAutenticacion Django application.
    
    Defines the application settings and metadata for the user authentication
    module, including field type defaults and application name.
    
    Attributes:
        default_auto_field: Specifies the default primary key field type
                           for models in this application
        name: The fully qualified name of the application module
    
    Purpose:
        - Configures database field defaults for optimal performance
        - Enables Django's application registry to properly manage the module
        - Provides namespace isolation for authentication functionality
        - Supports Django's app-level configuration and initialization
        - Integrates with Django's authentication framework
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apiAutenticacion'
