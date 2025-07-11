import environ
import os
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout, get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserUpdateSerializer, UserSerializer

# Usar el modelo de usuario configurado
User = get_user_model()

env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

class UserRegisterView(generics.CreateAPIView):
    """
        Vista para registrar nuevos usuarios.

        Endpoint: POST /auth/register/

        Campos requeridos:
            - email: Email único del usuario
            - password: Contraseña
            - username: Nombre de usuario único
            - nombre: Nombre completo (opcional)

        Retorna:
            - Mensaje de éxito
            - Datos del usuario
            - Token de acceso JWT
            - Token de refresco JWT

        Permisos: Acceso público
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    """
        Vista para autenticar usuarios.

        Endpoint: POST /auth/login/

        Campos requeridos:
            - email: Email del usuario
            - password: Contraseña

        Retorna:
            - Mensaje de éxito
            - Datos del usuario
            - Token de acceso JWT
            - Token de refresco JWT

        Permisos: Acceso público
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login exitoso',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveAPIView):
    """
        Vista para obtener el perfil del usuario autenticado.

        Endpoint: GET /auth/profile/

        Retorna:
            Datos completos del usuario actual

        Permisos: Usuario autenticado
        Requiere: Token JWT válido
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UpdateUserInfo(generics.UpdateAPIView):
    """
        Vista para actualizar información del usuario.

        Endpoint: PUT/PATCH /auth/update/

        Campos modificables:
            - username: Nuevo nombre de usuario
            - email: Nuevo email
            - nombre: Nuevo nombre completo

        Retorna:
            - Mensaje de éxito
            - Datos actualizados

        Permisos: Usuario autenticado
        Requiere: Token JWT válido
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
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
        Vista para cerrar sesión de usuario.

        Endpoint: POST /auth/logout/

        Campos requeridos:
            - refresh: Token de refresco JWT

        Acciones:
            - Invalida el token JWT
            - Cierra la sesión del usuario

        Retorna:
            Mensaje de confirmación

        Permisos: Acceso público
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            logout(request)
            return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Error en logout'}, status=status.HTTP_400_BAD_REQUEST)
