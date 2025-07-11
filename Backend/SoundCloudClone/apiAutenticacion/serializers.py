from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

# Usar el modelo de usuario configurado
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    """
        Serializador para el registro de nuevos usuarios.

        Campos:
            email (EmailField): Email único del usuario
            password (CharField): Contraseña (mínimo 8 caracteres)
            username (CharField): Nombre de usuario único
            nombre (CharField): Nombre completo (opcional)

        Validaciones:
            - Email único en el sistema
            - Contraseña con mínimo 8 caracteres
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
                Crea un nuevo usuario con los datos validados.

                Args:
                    validated_data (dict): Datos validados del usuario

                Returns:
                    User: Nueva instancia de usuario creada
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
        Serializador para la autenticación de usuarios.

        Campos:
            email (EmailField): Email del usuario
            password (CharField): Contraseña

        Validaciones:
            - Verifica credenciales mediante authenticate
            - Comprueba si la cuenta está activa
            - Requiere ambos campos email y password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        """
                Valida las credenciales del usuario.

                Args:
                    attrs (dict): Datos de autenticación

                Returns:
                    dict: Datos validados con el usuario autenticado

                Raises:
                    ValidationError: Si las credenciales son inválidas o la cuenta está inactiva
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
        Serializador para mostrar información del usuario.

        Campos:
            user_id (AutoField): ID único del usuario
            username (CharField): Nombre de usuario
            email (EmailField): Email del usuario
            nombre (CharField): Nombre completo
            created_at (DateTimeField): Fecha de creación
    """
    class Meta:
        """
            Serializador para actualizar datos del usuario.

            Campos:
                username (CharField): Nombre de usuario
                email (EmailField): Email del usuario
                nombre (CharField): Nombre completo

            Notas:
                - No permite modificar la contraseña
                - Mantiene las validaciones de unicidad
        """
        model = User
        fields = ('user_id', 'username', 'email', 'nombre', 'created_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['username', 'email', 'nombre']