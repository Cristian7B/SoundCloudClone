"""
API views for user authentication and profile management.

This module contains all the view classes that handle user authentication operations
including registration, login, logout, profile retrieval, and profile updates.
All views are built using Django REST Framework's generic views for consistency
and maintainability.

Classes:
    UserRegisterView: Handles user registration with email notifications
    UserLoginView: Handles user authentication and JWT token generation
    UserProfileView: Retrieves authenticated user's profile information
    UpdateUserInfo: Handles user profile updates
    UserLogout: Handles user logout and token blacklisting
    UserNombreView: Retrieves basic user information by user ID

Features:
    - JWT token generation and management
    - Email notifications for new user registrations
    - Secure password handling
    - Token blacklisting for logout
    - Profile management capabilities

@author: Development Team
@version: 1.0
@since: 2024
"""

import environ
import os
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout, get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserUpdateSerializer, UserSerializer, UserNombreSerializer
from .email_utils import EmailService

# Use the configured custom user model
User = get_user_model()

# Load environment variables for configuration
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))


class UserRegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    
    Handles the creation of new user accounts including password hashing,
    JWT token generation, and welcome email sending. Open to all users
    (no authentication required).
    
    Endpoint: POST /usuarios/registro/
    
    Request Body:
        {
            "username": "johndoe",
            "email": "john@example.com",
            "nombre": "John Doe",
            "password": "securepassword123"
        }
    
    Response:
        {
            "message": "Usuario registrado exitosamente",
            "user": {
                "user_id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "nombre": "John Doe",
                "created_at": "2024-01-01T00:00:00Z"
            },
            "refresh": "jwt_refresh_token",
            "access": "jwt_access_token",
            "email_message": "Email de bienvenida enviado a john@example.com"
        }
    
    Features:
        - Validates user input using UserRegisterSerializer
        - Creates user account with hashed password
        - Generates JWT access and refresh tokens
        - Sends welcome email notification
        - Returns user data and authentication tokens
    
    Permissions:
        - AllowAny: No authentication required for registration
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create a new user account with email notification.
        
        Args:
            request: HTTP request containing user registration data
            
        Returns:
            Response: JSON response with user data, tokens, and email status
            
        Raises:
            ValidationError: If user input is invalid
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send welcome email notification
        email_sent = EmailService.send_welcome_email(user)
        
        # Generate JWT tokens for immediate authentication
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        # Add email status to response
        if email_sent:
            response_data['email_message'] = f'Email de bienvenida enviado a {user.email}'
        else:
            response_data['email_message'] = 'Usuario creado pero hubo un problema enviando el email de bienvenida'
        
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    API view for user authentication.
    
    Handles user login by validating credentials and generating JWT tokens.
    Uses email and password for authentication instead of username.
    
    Endpoint: POST /usuarios/login/
    
    Request Body:
        {
            "email": "john@example.com",
            "password": "securepassword123"
        }
    
    Response:
        {
            "message": "Login exitoso",
            "user": {
                "user_id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "nombre": "John Doe",
                "created_at": "2024-01-01T00:00:00Z"
            },
            "refresh": "jwt_refresh_token",
            "access": "jwt_access_token"
        }
    
    Features:
        - Validates credentials using Django's authentication backend
        - Generates new JWT access and refresh tokens
        - Returns user profile data with tokens
        - Checks for active user account status
    
    Permissions:
        - AllowAny: No authentication required for login
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Authenticate user and generate JWT tokens.
        
        Args:
            request: HTTP request containing login credentials
            
        Returns:
            Response: JSON response with user data and authentication tokens
            
        Raises:
            ValidationError: If credentials are invalid or user is inactive
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Generate JWT tokens for authenticated user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login exitoso',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    """
    API view for retrieving authenticated user's profile.
    
    Returns the profile information of the currently authenticated user.
    Requires valid JWT token in the Authorization header.
    
    Endpoint: GET /usuarios/perfil/
    
    Headers:
        Authorization: Bearer <jwt_access_token>
    
    Response:
        {
            "user_id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "nombre": "John Doe",
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    Features:
        - Returns complete user profile data
        - Automatically retrieves current authenticated user
        - Secure access through JWT authentication
    
    Permissions:
        - IsAuthenticated: Requires valid JWT token
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return the current authenticated user.
        
        Returns:
            User: The authenticated user instance
        """
        return self.request.user


class UpdateUserInfo(generics.UpdateAPIView):
    """
    API view for updating user profile information.
    
    Allows authenticated users to update their profile data including
    username, email, and display name. Supports both full and partial updates.
    
    Endpoints:
        PUT /usuarios/actualizar/ - Full update (all fields required)
        PATCH /usuarios/actualizar/ - Partial update (only provided fields)
    
    Headers:
        Authorization: Bearer <jwt_access_token>
    
    Request Body (example for partial update):
        {
            "nombre": "New Display Name",
            "email": "newemail@example.com"
        }
    
    Response:
        {
            "message": "Perfil actualizado exitosamente",
            "user": {
                "username": "johndoe",
                "email": "newemail@example.com",
                "nombre": "New Display Name"
            }
        }
    
    Features:
        - Supports partial updates (PATCH) and full updates (PUT)
        - Validates updated data using UserUpdateSerializer
        - Automatically targets current authenticated user
        - Returns success message with updated user data
    
    Permissions:
        - IsAuthenticated: Requires valid JWT token
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return the current authenticated user for updating.
        
        Returns:
            User: The authenticated user instance to be updated
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Update user profile information.
        
        Args:
            request: HTTP request containing updated user data
            
        Returns:
            Response: JSON response with success message and updated user data
            
        Note:
            Supports both partial (PATCH) and full (PUT) updates.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Perfil actualizado exitosamente',
            'user': serializer.data
        }, status=status.HTTP_200_OK)


class UserLogout(generics.GenericAPIView):
    """
    API view for user logout and token management.
    
    Handles user logout by blacklisting the provided refresh token
    and clearing the user session. This ensures the token cannot
    be used for future authentication.
    
    Endpoint: POST /usuarios/logout/
    
    Request Body:
        {
            "refresh": "jwt_refresh_token"
        }
    
    Response:
        {
            "message": "Logout exitoso"
        }
    
    Features:
        - Blacklists provided refresh token for security
        - Clears user session
        - Graceful error handling for invalid tokens
        - Works with or without providing refresh token
    
    Permissions:
        - AllowAny: No authentication required (uses provided token)
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Log out user and blacklist refresh token.
        
        Args:
            request: HTTP request containing refresh token
            
        Returns:
            Response: JSON response with logout status
            
        Note:
            If refresh token is provided, it will be blacklisted.
            If no token or invalid token, still clears session.
        """
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            logout(request)
            return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Error en logout'}, status=status.HTTP_400_BAD_REQUEST)


class UserNombreView(generics.RetrieveAPIView):
    """
    API view for retrieving basic user information by user ID.
    
    Returns minimal user information including ID, display name, and username.
    Used for displaying user information in contexts where only basic
    identification is needed (e.g., song credits, playlist ownership).
    
    Endpoint: GET /usuarios/{user_id}/nombre/
    
    URL Parameters:
        user_id (int): The unique identifier of the user
    
    Response:
        {
            "user_id": 1,
            "nombre": "John Doe",
            "username": "johndoe"
        }
    
    Error Response:
        {
            "error": "Usuario no encontrado"
        }
    
    Features:
        - Public endpoint (no authentication required)
        - Lightweight response with minimal user data
        - Proper error handling for non-existent users
        - Uses user_id for lookup instead of username
    
    Permissions:
        - AllowAny: Public endpoint for user identification
    
    Use Cases:
        - Displaying song/playlist creators
        - User mentions in comments
        - Public user directory
        - Attribution in content sharing
    """
    queryset = User.objects.all()
    serializer_class = UserNombreSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user_id'
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve basic user information by user ID.
        
        Args:
            request: HTTP request
            user_id: User ID from URL parameters
            
        Returns:
            Response: JSON response with user information or error message
            
        Raises:
            Http404: If user with given ID does not exist
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            return Response({
                'user_id': instance.user_id,
                'nombre': instance.nombre,
                'username': instance.username
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
