"""
ASGI configuration for SoundCloudClone project.

ASGI (Asynchronous Server Gateway Interface) is a spiritual successor to WSGI,
designed to provide a standard interface between async-capable Python web servers,
frameworks, and applications. This configuration enables the SoundCloud clone to
handle both synchronous and asynchronous requests efficiently.

This module exposes the ASGI callable as a module-level variable named 'application'.
The ASGI application handles HTTP requests, WebSocket connections, and other
protocol types in an asynchronous manner, providing better performance for
concurrent connections.

Key Features:
    - Asynchronous request handling for improved performance
    - WebSocket support for real-time features (future implementation)
    - Compatibility with modern deployment platforms
    - Scalable architecture for high-traffic scenarios

Deployment Considerations:
    - Compatible with ASGI servers like Uvicorn, Hypercorn, or Daphne
    - Supports both development and production environments
    - Enables real-time features like live chat, notifications, and streaming
    - Optimized for cloud deployments and containerized applications

Usage:
    This module is typically used by ASGI servers to serve the Django application:
    
    # Development with Uvicorn
    uvicorn SoundCloudClone.asgi:application --reload
    
    # Production deployment
    uvicorn SoundCloudClone.asgi:application --host 0.0.0.0 --port 8000

Future Enhancements:
    - WebSocket consumers for real-time music streaming
    - Live chat functionality for social features
    - Real-time notifications for user interactions
    - Live playlist collaboration features

@author: Development Team
@version: 1.0
@since: Django 5.2.3
@see: https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set default Django settings module for the ASGI application
# This ensures the application uses the correct configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoundCloudClone.settings')

# Create and configure the ASGI application
# This callable handles all incoming requests and routes them appropriately
application = get_asgi_application()
