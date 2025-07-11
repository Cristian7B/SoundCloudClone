"""
Serializers for the authentication API module.

This module contains all the serializers used for user authentication operations
including user registration, login, profile management, and user data updates.
The serializers handle data validation, transformation, and creation of user instances.

Classes:
    UserRegisterSerializer: Handles user registration with validation
    UserLoginSerializer: Handles user login authentication
    UserSerializer: Standard user data serialization
    UserUpdateSerializer: Handles user profile updates
    UserNombreSerializer: Lightweight serializer for user names

@author: Development Team
@version: 1.0
@since: 2024
"""

from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

# Use the configured custom user model
User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles the creation of new user accounts with proper validation
    including email uniqueness, password strength, and optional name field.
    
    Fields:
        email (EmailField): User's email address (required, unique)
        password (CharField): User's password (required, min 8 characters, write-only)
        nombre (CharField): User's display name (optional, defaults to username)
        username (CharField): User's unique username (required)
    
    Validation:
        - Email must be unique across all users
        - Password must be at least 8 characters long
        - Username is validated by Django's default validators
    
    Example:
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'nombre': 'John Doe',
            'password': 'securepassword123'
        }
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    nombre = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'nombre', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Create and return a new user instance.
        
        Args:
            validated_data (dict): Validated data from the serializer
            
        Returns:
            User: The newly created user instance
            
        Note:
            If 'nombre' is not provided, defaults to the username value.
            Password is automatically hashed using Django's create_user method.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nombre=validated_data.get('nombre', validated_data['username']),
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication.
    
    Handles user login by validating email and password credentials.
    Uses Django's authentication backend to verify user credentials.
    
    Fields:
        email (EmailField): User's email address for authentication
        password (CharField): User's password for authentication
    
    Validation:
        - Both email and password are required
        - Credentials must match an existing active user
        - User account must be active (not deactivated)
    
    Returns:
        dict: Validated data including the authenticated user instance
    
    Raises:
        ValidationError: If credentials are invalid or user is inactive
    
    Example:
        data = {'email': 'john@example.com', 'password': 'securepassword123'}
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate user credentials and return user instance.
        
        Args:
            attrs (dict): Dictionary containing email and password
            
        Returns:
            dict: Validated attributes including user instance
            
        Raises:
            ValidationError: If credentials are invalid, missing, or user is inactive
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            if not user:
                raise ValidationError('Credenciales inválidas')
            if not user.is_active:
                raise ValidationError('Cuenta desactivada')
            attrs['user'] = user
            return attrs
        else:
            raise ValidationError('Debe incluir email y password')


class UserSerializer(serializers.ModelSerializer):
    """
    Standard serializer for user data representation.
    
    Used for displaying user information in API responses.
    Includes read-only fields that are safe to expose publicly.
    
    Fields:
        user_id (int): User's unique identifier
        username (str): User's unique username
        email (str): User's email address
        nombre (str): User's display name
        created_at (datetime): Account creation timestamp
    
    Note:
        This serializer is read-only and should be used for displaying
        user information rather than creating or updating users.
    """
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'nombre', 'created_at')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    
    Allows users to update their profile data including username,
    email, and display name. Excludes sensitive fields like password.
    
    Fields:
        username (str): User's unique username
        email (str): User's email address
        nombre (str): User's display name
    
    Validation:
        - Username must remain unique if changed
        - Email must remain unique if changed
        - All Django model validations apply
    
    Example:
        data = {'nombre': 'New Display Name', 'email': 'newemail@example.com'}
        serializer = UserUpdateSerializer(user_instance, data=data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
    """
    class Meta: 
        model = User
        fields = ['username', 'email', 'nombre']


class UserNombreSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for user identification.
    
    Returns minimal user information including ID, display name, and username.
    Used in contexts where only basic user identification is needed,
    such as in song/playlist ownership displays or user mentions.
    
    Fields:
        user_id (int): User's unique identifier
        nombre (str): User's display name
        username (str): User's unique username
    
    Use Cases:
        - Displaying song/playlist creators
        - User search results
        - Comments and interaction attribution
        - Any scenario requiring minimal user info
    
    Example:
        users = User.objects.filter(username__icontains=query)
        serializer = UserNombreSerializer(users, many=True)
        return Response(serializer.data)
    """
    class Meta:
        model = User
        fields = ['user_id', 'nombre', 'username']