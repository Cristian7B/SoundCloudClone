"""
Django settings configuration for SoundCloudClone project.

This module contains all the configuration settings for the SoundCloud clone application,
including database configuration, authentication settings, email settings, CORS settings,
and JWT token configuration.

The application is structured with multiple Django apps:
- apiAutenticacion: Handles user authentication and registration
- apiBuscar: Provides search functionality for songs and content
- apiDatabase: Manages database operations and models
- apiPersistencia: Handles data persistence for songs, playlists, and albums
- apiSugerenciaCanciones: Provides song recommendation functionality
- apiSugerenciaPlaylists: Provides playlist recommendation functionality

Key Features:
- Custom user model (AppUser) for extended authentication
- JWT-based authentication with token refresh and blacklisting
- PostgreSQL database configuration with environment variables
- Email configuration for user notifications
- CORS configuration for frontend integration
- REST framework integration with proper authentication classes

Environment Variables Required:
- EMAIL_HOST_USER: Gmail account for sending emails
- EMAIL_HOST_PASSWORD: Gmail app password for SMTP authentication
- DB_NAME: PostgreSQL database name
- DB_USER: PostgreSQL username
- DB_PASSWORD: PostgreSQL password
- DB_HOST: PostgreSQL host (usually localhost)
- DB_PORT: PostgreSQL port (usually 5432)

@author: Development Team
@version: 1.0
@since: Django 5.2.3
"""

from pathlib import Path
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables handler
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")


# SECURITY SETTINGS
# ================================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing and should be kept secure in production
SECRET_KEY = 'django-insecure-ntvgj%_vnz3$ayx^)-03g=)-zk(5+2k9+a=3b1!#2a&xb@&7x^'

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode provides detailed error information but should be disabled in production
DEBUG = True

# Hosts/domain names that this Django site can serve
# Should be configured properly in production for security
ALLOWED_HOSTS = []


# EMAIL CONFIGURATION
# ================================================================================

# Email backend configuration for sending notifications and welcome emails
# Uses Gmail SMTP for production, can be switched to console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')  # Gmail address from environment
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')  # Gmail app password from environment

# Email encoding and timezone settings
EMAIL_USE_LOCALTIME = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# Internationalization settings
USE_I18N = True
USE_TZ = True



# APPLICATION DEFINITION
# ================================================================================

# Django applications that are installed and enabled for this project
# Includes both Django built-in apps and custom apps for the SoundCloud clone
INSTALLED_APPS = [
    'django.contrib.admin',          # Django admin interface
    'django.contrib.auth',           # Django authentication framework
    'django.contrib.contenttypes',   # Content type framework
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file handling
    'corsheaders',                   # CORS headers for frontend integration
    
    # Custom applications for SoundCloud clone functionality
    'apiAutenticacion',              # User authentication and registration
    'apiBuscar',                     # Search functionality for content
    'apiDatabase',                   # Database operations and models
    'apiPersistencia',               # Data persistence for songs, playlists, albums
    'apiSugerenciaCanciones',        # Song recommendation system
    'apiSugerenciaPlaylists',        # Playlist recommendation system
    
    # Third-party packages for API and authentication
    'rest_framework',                # Django REST framework for API development
    'rest_framework_simplejwt',      # JWT authentication for REST API
    'rest_framework_simplejwt.token_blacklist',  # Token blacklisting for security
]

# REST Framework configuration
# Defines the default authentication classes for API endpoints
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Middleware configuration
# Defines the middleware stack that processes requests and responses
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',              # CORS handling (must be first)
    'django.middleware.security.SecurityMiddleware',      # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',          # Common functionality
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',     # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking protection
]

# Root URL configuration
ROOT_URLCONF = 'SoundCloudClone.urls'

# Template configuration
# Currently using default Django templates with app directories enabled
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'SoundCloudClone.wsgi.application'


# CUSTOM USER MODEL
# ================================================================================

# Custom user model that extends Django's built-in user functionality
# Provides additional fields and methods specific to the SoundCloud clone
AUTH_USER_MODEL = 'apiAutenticacion.AppUser'

# DATABASE CONFIGURATION
# ================================================================================

# Database configuration using PostgreSQL
# Credentials are loaded from environment variables for security
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"),        # Database name from environment
        'USER': env("DB_USER"),        # Database username from environment
        'PASSWORD': env("DB_PASSWORD"), # Database password from environment
        'HOST': env("DB_HOST"),        # Database host from environment
        'PORT': env("DB_PORT"),        # Database port from environment
    }
}


# PASSWORD VALIDATION
# ================================================================================

# Password validation rules to ensure strong user passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# INTERNATIONALIZATION
# ================================================================================

# Language and timezone configuration
LANGUAGE_CODE = 'en-us'  # Default language
TIME_ZONE = 'UTC'        # Default timezone
USE_I18N = True          # Enable internationalization
USE_TZ = True            # Enable timezone support


# STATIC FILES
# ================================================================================

# Static files (CSS, JavaScript, Images) configuration
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS CONFIGURATION
# ================================================================================

# CORS (Cross-Origin Resource Sharing) settings for frontend integration
# Allows frontend applications to make requests to the Django backend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React development server (default port)
    "http://127.0.0.1:3000",      # React development server (localhost alternative)
    "http://localhost:5173",      # Vite development server (default port)
    "http://127.0.0.1:5173",      # Vite development server (localhost alternative)
]

# Allow all origins for development - SHOULD BE DISABLED IN PRODUCTION
CORS_ALLOW_ALL_ORIGINS = True  # For development only


# JWT AUTHENTICATION CONFIGURATION
# ================================================================================

# JWT (JSON Web Token) settings for API authentication
from datetime import timedelta

SIMPLE_JWT = {
    # Token lifetime settings
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),    # Access token expires in 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),       # Refresh token expires in 1 day
    'ROTATE_REFRESH_TOKENS': True,                     # Generate new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,                  # Blacklist old refresh tokens
    'UPDATE_LAST_LOGIN': False,                        # Don't update last_login field
    
    # Signing algorithm and key
    'ALGORITHM': 'HS256',                              # HMAC SHA-256 algorithm
    'SIGNING_KEY': SECRET_KEY,                         # Use Django secret key for signing
    'VERIFYING_KEY': None,                             # Not needed for HMAC algorithms
    'AUDIENCE': None,                                  # JWT audience claim
    'ISSUER': None,                                    # JWT issuer claim
    'JWK_URL': None,                                   # JSON Web Key URL
    'LEEWAY': 0,                                       # Clock skew tolerance
    
    # Token headers and claims
    'AUTH_HEADER_TYPES': ('Bearer',),                  # Authorization header type
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',          # Authorization header name
    'USER_ID_FIELD': 'user_id',                        # User model field for user ID
    'USER_ID_CLAIM': 'user_id',                        # JWT claim for user ID
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    # Token classes and types
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',                  # Claim for token type
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    # Additional claims
    'JTI_CLAIM': 'jti',                               # JSON Token Identifier claim
    
    # Sliding token settings (alternative to access/refresh token pattern)
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
