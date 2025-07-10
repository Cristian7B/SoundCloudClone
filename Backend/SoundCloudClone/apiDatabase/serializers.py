from rest_framework import serializers
from .models import EstadisticasGenerales, RegistroActividad, ConfiguracionSistema
from apiPersistencia.models import Cancion, Playlist
from django.contrib.auth import get_user_model

# Usar el modelo de usuario configurado
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = User
        fields = ('username', 'nombre', 'email')

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'

class RegistroCancion(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = ('titulo', 'archivo_url', 'usuario_id')

class RegistroPlayList(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('titulo', 'usuario_id')

class EstadisticasGeneralesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadisticasGenerales
        fields = '__all__'

class RegistroActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroActividad
        fields = '__all__'

class ConfiguracionSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionSistema
        fields = '__all__'
