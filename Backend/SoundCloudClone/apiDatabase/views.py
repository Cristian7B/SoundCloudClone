from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import *
from .models import *
from apiPersistencia.models import Cancion, Playlist

User = get_user_model()

class RegistroCancionView(generics.CreateAPIView):
    """
        Vista para registrar nuevas canciones.

        Endpoint: POST /database/cancion/

        Campos requeridos:
            - titulo: Título de la canción
            - archivo_url: URL del archivo de audio

        Retorna:
            - Mensaje de éxito
            - Datos de la canción registrada

        Permisos: Usuario autenticado
        Requiere: Token JWT válido
        """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = RegistroCancion(data=request.data)
        if serializer.is_valid():
            # Asignar el usuario autenticado
            cancion = serializer.save(usuario_id=request.user.user_id)
            return Response({
                'message': 'La canción se ha registrado exitosamente',
                'cancion': CancionSerializer(cancion).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'No se pudo registrar la canción',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RegistroPlayListView(generics.CreateAPIView):
    """
        Vista para crear nuevas playlists.

        Endpoint: POST /database/playlist/

        Campos requeridos:
            - titulo: Nombre de la playlist

        Retorna:
            - Mensaje de éxito
            - Datos de la playlist creada

        Permisos: Usuario autenticado
        Requiere: Token JWT válido
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = RegistroPlayList(data=request.data)
        if serializer.is_valid():
            # Asignar el usuario autenticado
            playlist = serializer.save(usuario_id=request.user.user_id)
            return Response({
                'message': 'La playlist se ha creado exitosamente',
                'playlist': PlaylistSerializer(playlist).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'No se pudo crear la playlist',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class GetUserInfo(generics.RetrieveAPIView):
    """
        Vista para obtener información del usuario.

        Endpoint: GET /database/user/info/

        Retorna:
            - user_id: ID del usuario
            - email: Correo electrónico
            - username: Nombre de usuario
            - nombre: Nombre completo
            - created_at: Fecha de creación

        Permisos: Usuario autenticado
        Requiere: Token JWT válido
    """

    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        try:
            user_data = {
                'user_id': user.user_id,
                'email': user.email,
                'username': user.username,
                'nombre': user.nombre,
                'created_at': user.created_at,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Error obteniendo información del usuario'
            }, status=status.HTTP_404_NOT_FOUND)

class UpdateUserInfo(generics.UpdateAPIView):
    """
        Vista para actualizar datos del usuario.

        Endpoint: PATCH /database/user/update/

        Campos modificables:
            - username: Nombre de usuario
            - email: Correo electrónico
            - nombre: Nombre completo

        Permisos: Usuario autenticado
        Requiere: Token JWT válido
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        return self.request.user
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class LoginUser(generics.GenericAPIView):
    """
        Vista para autenticar usuarios.

        Endpoint: POST /database/login/

        Campos requeridos:
            - email: Correo electrónico
            - password: Contraseña

        Retorna:
            - Tokens JWT (acceso y refresco)
            - Datos del usuario autenticado

        Permisos: Acceso público
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'user_id': user.user_id,
                        'email': user.email,
                        'username': user.username,
                        'nombre': user.nombre,
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Credenciales inválidas'
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_400_BAD_REQUEST)

class CheckUserExist(generics.GenericAPIView):
    """
        Vista para verificar existencia de usuario.

        Endpoint: GET /database/user/check/?email={email}

        Parámetros:
            email (str): Correo electrónico a verificar

        Retorna:
            - exists: Boolean indicando existencia
            - user: Datos del usuario si existe

        Permisos: Acceso público
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        email = request.query_params.get('email')
        
        if not email:
            return Response({
                'error': 'Email es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            return Response({
                'exists': True,
                'user': {
                    'user_id': user.user_id,
                    'email': user.email,
                    'username': user.username,
                    'nombre': user.nombre,
                }
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'exists': False
            }, status=status.HTTP_200_OK)
