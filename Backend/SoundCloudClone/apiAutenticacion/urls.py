"""
URL configuration for the authentication API module.

This module defines URL patterns for all user authentication and profile management
endpoints. Provides comprehensive user account functionality including registration,
login, profile management, and JWT token handling.

Endpoints Overview:
    - User registration with email notifications
    - Email-based login with JWT token generation
    - Profile retrieval and updates for authenticated users
    - Secure logout with token blacklisting
    - JWT token refresh for session management
    - Public user information lookup by ID

Security Features:
    - JWT-based authentication for protected endpoints
    - Token blacklisting for secure logout
    - Permission-based access control
    - Email verification and welcome notifications

URL Patterns:
    register/ - User account creation
    login/ - User authentication
    profile/ - Current user profile access
    update-info/ - Profile information updates
    logout/ - Session termination
    token/refresh/ - JWT token renewal
    usuarios/{user_id}/nombre/ - Public user information lookup

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.urls import path
from .views import (
    UserRegisterView, UserLoginView, UpdateUserInfo, UserLogout, UserProfileView, 
    UserNombreView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User Registration
    # POST /api/auth/register/ - Create new user account with email notification
    # Public endpoint that creates user and returns JWT tokens
    path('register/', UserRegisterView.as_view(), name='register'),
    
    # User Login
    # POST /api/auth/login/ - Authenticate user with email and password
    # Public endpoint that validates credentials and returns JWT tokens
    path('login/', UserLoginView.as_view(), name='login'),
    
    # User Profile Retrieval
    # GET /api/auth/profile/ - Get current authenticated user's profile
    # Protected endpoint requiring valid JWT token
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    
    # Profile Information Update
    # PUT/PATCH /api/auth/update-info/ - Update user profile information
    # Protected endpoint for authenticated users only
    path('update-info/', UpdateUserInfo.as_view(), name='update_info'),
    
    # User Logout
    # POST /api/auth/logout/ - Logout user and blacklist refresh token
    # Public endpoint that accepts refresh token for blacklisting
    path('logout/', UserLogout.as_view(), name='logout'),
    
    # JWT Token Refresh
    # POST /api/auth/token/refresh/ - Refresh access token using refresh token
    # Public endpoint provided by django-rest-framework-simplejwt
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Public User Information
    # GET /api/auth/usuarios/{user_id}/nombre/ - Get basic user info by ID
    # Public endpoint for displaying user names in content attribution
    path('usuarios/<int:user_id>/nombre/', UserNombreView.as_view(), name='user_nombre'),
]
