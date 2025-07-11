#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks in SoundCloudClone.

This script serves as the primary entry point for all Django management commands
including database migrations, server startup, user creation, and custom management
commands. It provides a convenient interface for development, testing, and
deployment operations.

Common Commands:
    python manage.py runserver - Start development server
    python manage.py migrate - Apply database migrations
    python manage.py makemigrations - Create new migrations
    python manage.py createsuperuser - Create admin user
    python manage.py collectstatic - Collect static files
    python manage.py test - Run test suite
    python manage.py shell - Open Django shell
    python manage.py dbshell - Open database shell

Development Workflow:
    1. python manage.py makemigrations - After model changes
    2. python manage.py migrate - Apply database changes
    3. python manage.py runserver - Start development server
    4. python manage.py test - Run tests before deployment

Database Management:
    - migrate: Apply pending migrations to database
    - makemigrations: Generate migration files from model changes
    - showmigrations: Display migration status
    - sqlmigrate: Show SQL for specific migration

User Management:
    - createsuperuser: Create admin account for Django admin
    - changepassword: Change user password
    - createcachetable: Create cache tables if using database caching

Static Files:
    - collectstatic: Gather static files for production
    - findstatic: Locate static files
    - runserver: Serve static files in development

Environment Setup:
    Ensure the following before running commands:
    - Virtual environment is activated
    - Required packages are installed (pip install -r requirements.txt)
    - Database is configured and accessible
    - Environment variables are set (.env file)

Error Handling:
    - Provides clear error messages for Django import issues
    - Suggests virtual environment activation if Django is not found
    - Includes original exception context for debugging

@author: Development Team
@version: 1.0
@since: Django 5.2.3
"""

import os
import sys


def main():
    """
    Run administrative tasks for the SoundCloudClone Django project.
    
    This function sets up the Django environment and executes command-line
    management commands. It handles environment configuration and provides
    helpful error messages for common setup issues.
    
    Environment Variables:
        DJANGO_SETTINGS_MODULE: Points to the settings configuration
                               (defaults to 'SoundCloudClone.settings')
    
    Raises:
        ImportError: If Django is not installed or not accessible
                    Usually indicates missing virtual environment activation
    
    Examples:
        # Start development server
        python manage.py runserver
        
        # Create and apply migrations
        python manage.py makemigrations
        python manage.py migrate
        
        # Create admin user
        python manage.py createsuperuser
        
        # Run tests
        python manage.py test
    """
    # Set default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoundCloudClone.settings')
    
    try:
        # Import Django's command-line management utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide helpful error message for Django import issues
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the requested management command
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
