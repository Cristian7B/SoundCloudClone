"""
WSGI configuration for SoundCloudClone project.

WSGI (Web Server Gateway Interface) is a Python specification that describes
how a web server communicates with web applications. This configuration provides
the entry point for traditional synchronous web servers to serve the SoundCloud
clone Django application.

This module exposes the WSGI callable as a module-level variable named 'application'.
The WSGI application handles HTTP requests in a synchronous manner, making it
compatible with traditional web servers like Apache, Nginx with uWSGI, or Gunicorn.

Key Features:
    - Synchronous request handling for traditional deployment scenarios
    - Wide compatibility with existing web server infrastructure
    - Proven stability for production environments
    - Simple configuration and deployment process

Deployment Scenarios:
    - Traditional web hosting environments
    - Apache with mod_wsgi
    - Nginx with uWSGI or Gunicorn
    - Cloud platforms supporting WSGI applications
    - Containerized deployments with traditional servers

Usage Examples:
    # Gunicorn deployment
    gunicorn SoundCloudClone.wsgi:application
    
    # uWSGI deployment
    uwsgi --module=SoundCloudClone.wsgi:application
    
    # Development with Django's built-in server
    python manage.py runserver

Performance Considerations:
    - Suitable for most web applications with moderate traffic
    - Can be scaled horizontally with load balancers
    - Memory usage is predictable and manageable
    - CPU usage scales linearly with request volume

Note:
    For applications requiring real-time features or handling many concurrent
    connections, consider using the ASGI configuration instead, which provides
    better performance for asynchronous operations.

@author: Development Team
@version: 1.0
@since: Django 5.2.3
@see: https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default Django settings module for the WSGI application
# This ensures the application uses the correct configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoundCloudClone.settings')

# Create and configure the WSGI application
# This callable handles all incoming HTTP requests
application = get_wsgi_application()

# Alternative reference for some deployment scenarios
# Some WSGI servers may expect the application to be named 'app'
app = application
