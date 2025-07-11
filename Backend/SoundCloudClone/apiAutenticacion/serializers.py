from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

# Usar el modelo de usuario configurado
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
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
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nombre=validated_data.get('nombre', validated_data['username']),
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
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
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'nombre', 'created_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['username', 'email', 'nombre']

class UserNombreSerializer(serializers.ModelSerializer):
    """
    Serializer para retornar solo el nombre del usuario
    """
    class Meta:
        model = User
        fields = ['user_id', 'nombre', 'username']