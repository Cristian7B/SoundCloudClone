"""
URL configuration for database operations and system administration API.

This module defines URL patterns for specialized database operations,
user management utilities, and system administration functions.

URL Groups:
    Content Registration:
        - register-song/: Alternative song registration endpoint
        - register-playlist/: Alternative playlist creation endpoint
    
    User Management:
        - user-info/: Authenticated user information retrieval
        - update-user/: User profile update functionality
        - login/: Alternative login endpoint
        - check-user/: User existence verification

Features:
    - Alternative content creation workflows
    - Administrative user management tools
    - Database operation utilities
    - Authentication helper endpoints
    - System administration functions

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.urls import path
from .views import (
    RegistroCancionView, 
    RegistroPlayListView, 
    GetUserInfo, 
    UpdateUserInfo, 
    LoginUser, 
    CheckUserExist
)

urlpatterns = [
    # Content Registration Endpoints
    # POST /api/database/register-song/ - Alternative song registration
    path('register-song/', RegistroCancionView.as_view(), name='register_song'),
    
    # POST /api/database/register-playlist/ - Alternative playlist creation
    path('register-playlist/', RegistroPlayListView.as_view(), name='register_playlist'),
    
    # User Management Endpoints
    # GET /api/database/user-info/ - Get authenticated user information
    path('user-info/', GetUserInfo.as_view(), name='get_user_info'),
    
    # PUT /api/database/update-user/ - Update user profile information
    path('update-user/', UpdateUserInfo.as_view(), name='update_user_info'),
    
    # Authentication Helper Endpoints
    # POST /api/database/login/ - Alternative user login
    path('login/', LoginUser.as_view(), name='login_user'),
    
    # POST /api/database/check-user/ - Check if user exists
    path('check-user/', CheckUserExist.as_view(), name='check_user_exists'),
]