from rest_framework import serializers
from .models import EstadisticasGenerales, RegistroActividad, ConfiguracionSistema
from apiPersistencia.models import Cancion, Playlist
from django.contrib.auth import get_user_model

# Usar el modelo de usuario configurado
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    """
        Serializador para el registro de usuarios.

        Campos:
            username (str): Nombre de usuario único
            email (str): Email del usuario
            nombre (str): Nombre completo
            password (str): Contraseña (mínimo 8 caracteres, write_only)

        Validaciones:
            - Password mínimo 8 caracteres
            - Email y username únicos
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'nombre', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            nombre=validated_data.get('nombre', validated_data['username']),
            password=validated_data['password']
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """
        Serializador para actualizar datos de usuario.

        Campos:
            username (str): Nombre de usuario
            nombre (str): Nombre completo
            email (str): Email del usuario
    """
    class Meta:
        model = User
        fields = ('username', 'nombre', 'email')

class CancionSerializer(serializers.ModelSerializer):
    """
        Serializador completo de canciones.

        Campos:
            Todos los campos del modelo Cancion
        """
    class Meta:
        model = Cancion
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    """
        Serializador completo de playlists.

        Campos:
            Todos los campos del modelo Playlist
    """
    class Meta:
        model = Playlist
        fields = '__all__'

class RegistroCancion(serializers.ModelSerializer):
    """
        Serializador simplificado para registros de canciones.

        Campos:
            titulo (str): Título de la canción
            archivo_url (str): URL del archivo de audio
            usuario_id (int): ID del usuario creador
    """
    class Meta:
        model = Cancion
        fields = ('titulo', 'archivo_url', 'usuario_id')

class RegistroPlayList(serializers.ModelSerializer):
    """
        Serializador simplificado para registros de playlists.

        Campos:
            titulo (str): Título de la playlist
            usuario_id (int): ID del usuario creador
    """
    class Meta:
        model = Playlist
        fields = ('titulo', 'usuario_id')

class EstadisticasGeneralesSerializer(serializers.ModelSerializer):
    """
        Serializador para estadísticas generales del sistema.

        Campos:
            Todos los campos del modelo EstadisticasGenerales
    """
    class Meta:
        model = EstadisticasGenerales
        fields = '__all__'

class RegistroActividadSerializer(serializers.ModelSerializer):
    """
        Serializador para registros de actividad del sistema.

        Campos:
            Todos los campos del modelo RegistroActividad
    """
    class Meta:
        model = RegistroActividad
        fields = '__all__'

class ConfiguracionSistemaSerializer(serializers.ModelSerializer):
    """
        Serializador para configuraciones del sistema.

        Campos:
            Todos los campos del modelo ConfiguracionSistema
    """
    class Meta:
        model = ConfiguracionSistema
        fields = '__all__'
