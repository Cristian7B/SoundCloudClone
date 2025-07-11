"""
Módulo de modelos para el sistema de autenticación de usuarios.

Este módulo contiene las clases relacionadas con la gestión de usuarios,
incluyendo el modelo de usuario personalizado y su manager correspondiente.

@author: SoundCloud Clone Team
@version: 1.0
@since: 2025-07-10
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class AppUserManager(BaseUserManager):
    """
    Manager personalizado para el modelo de usuario de la aplicación.
    
    Proporciona métodos para crear usuarios regulares y superusuarios
    con validaciones específicas del negocio.
    
    @extends BaseUserManager
    """
    
    def create_user(self, email, username, nombre=None, password=None):
        """
        Crea y guarda un usuario regular con los datos proporcionados.
        
        @param email: Dirección de correo electrónico del usuario (requerido)
        @type email: str
        @param username: Nombre de usuario único (requerido)
        @type username: str
        @param nombre: Nombre completo del usuario (opcional, usa username si no se proporciona)
        @type nombre: str
        @param password: Contraseña del usuario (requerido)
        @type password: str
        @return: Instancia del usuario creado
        @rtype: AppUser
        @raises ValueError: Si email o password no son proporcionados o email es inválido
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
        Crea y guarda un superusuario con privilegios administrativos.
        
        @param email: Dirección de correo electrónico del superusuario
        @type email: str
        @param username: Nombre de usuario único del superusuario
        @type username: str
        @param password: Contraseña del superusuario
        @type password: str
        @return: Instancia del superusuario creado
        @rtype: AppUser
        """
        user = self.create_user(email, username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser):
    """
    Modelo de usuario personalizado para la aplicación SoundCloud Clone.
    
    Extiende AbstractBaseUser para proporcionar un sistema de autenticación
    personalizado basado en email en lugar de username.
    
    @extends AbstractBaseUser
    """
    
    # Campos del modelo
    user_id = models.AutoField(primary_key=True, help_text="ID único del usuario")
    username = models.CharField(max_length=100, unique=True, help_text="Nombre de usuario único")
    nombre = models.CharField(max_length=100, help_text="Nombre completo del usuario")
    email = models.EmailField(unique=True, help_text="Dirección de correo electrónico única")
    is_active = models.BooleanField(default=True, help_text="Indica si el usuario está activo")
    is_admin = models.BooleanField(default=False, help_text="Indica si el usuario tiene privilegios administrativos")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación del usuario")
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha y hora de última actualización")

    # Configuración de autenticación
    USERNAME_FIELD = 'email'  # Campo usado para autenticación
    REQUIRED_FIELDS = ['username']  # Campos requeridos además del USERNAME_FIELD

    # Manager personalizado
    objects = AppUserManager()

    def __str__(self):
        """
        Representación en cadena del usuario.
        
        @return: Email del usuario
        @rtype: str
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Verifica si el usuario tiene un permiso específico.
        
        @param perm: Permiso a verificar
        @type perm: str
        @param obj: Objeto sobre el cual verificar el permiso (opcional)
        @type obj: Any
        @return: True si el usuario es admin, False en caso contrario
        @rtype: bool
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Verifica si el usuario tiene permisos para una aplicación específica.
        
        @param app_label: Etiqueta de la aplicación
        @type app_label: str
        @return: True si el usuario es admin, False en caso contrario
        @rtype: bool
        """
        return self.is_admin

    @property
    def is_staff(self):
        """
        Propiedad que indica si el usuario es staff.
        
        @return: True si el usuario es admin, False en caso contrario
        @rtype: bool
        """
        return self.is_admin

    class Meta:
        """
        Metadatos del modelo AppUser.
        """
        db_table = 'app_users'
        ordering = ['-created_at']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'soundcloud_users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'