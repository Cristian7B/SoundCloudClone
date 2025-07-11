from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class AppUserManager(BaseUserManager):
    """
        Gestor personalizado para el modelo de usuario.
        Maneja la creación de usuarios normales y superusuarios.

        Métodos:
            create_user: Crea un usuario normal
            create_superuser: Crea un usuario administrador
    """
    def create_user(self, email, username, nombre=None, password=None):
        """
            Crea y guarda un nuevo usuario.

            Args:
                email (str): Email del usuario (requerido)
                username (str): Nombre de usuario único (requerido)
                nombre (str): Nombre completo (opcional)
                password (str): Contraseña (requerida)

            Returns:
                AppUser: Nueva instancia de usuario

            Raises:
                ValueError: Si falta email o contraseña, o si el email no es válido
        """
        if not email:
            raise ValueError('The Email Field must be set')
        if not password: 
            raise ValueError('The password must be set')
        
        email = self.normalize_email(email)

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('The email is not valid')

        user = self.model(
            email=email, 
            username=username,
            nombre=nombre or username
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, username, password=None):
        """
                Crea y guarda un superusuario.

                Args:
                    email (str): Email del administrador
                    username (str): Nombre de usuario
                    password (str): Contraseña

                Returns:
                    AppUser: Nueva instancia de superusuario
        """
        user = self.create_user(email, username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class AppUser(AbstractBaseUser):
    """
        Modelo personalizado de usuario que extiende AbstractBaseUser.

        Atributos:
            user_id (AutoField): Identificador único del usuario
            username (CharField): Nombre de usuario único
            nombre (CharField): Nombre completo del usuario
            email (EmailField): Email único del usuario
            is_active (BooleanField): Estado de la cuenta (activa/inactiva)
            is_admin (BooleanField): Indica si el usuario es administrador
            created_at (DateTimeField): Fecha de creación de la cuenta
            updated_at (DateTimeField): Fecha de última actualización

        Configuración:
            USERNAME_FIELD: Usa 'email' como campo de inicio de sesión
            REQUIRED_FIELDS: Campos adicionales requeridos al crear usuario
    """
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AppUserManager()

    def __str__(self):
        """
        Representación en string del usuario.

        Returns:
            str: Email del usuario
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
                Verifica permisos del usuario.
                Por defecto otorga todos los permisos.

                Returns:
                    bool: True
        """
        return True

    def has_module_perms(self, app_label):
        """
                Verifica permisos de módulo.
                Por defecto otorga acceso a todos los módulos.

                Returns:
                    bool: True
        """
        return True

    @property
    def is_staff(self):
        """
                Determina si el usuario tiene acceso al admin.

                Returns:
                    bool: True si el usuario es administrador
        """
        return self.is_admin

    class Meta:
        """
                Metaclase con configuraciones del modelo.

                Atributos:
                    db_table: Nombre de la tabla en la base de datos
                    verbose_name: Nombre singular para el admin
                    verbose_name_plural: Nombre plural para el admin
        """
        db_table = 'soundcloud_users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'