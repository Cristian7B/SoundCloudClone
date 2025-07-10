from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class AppUserManager(BaseUserManager):
    def create_user(self, email, username, nombre=None, password=None):
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
        user = self.create_user(email, username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class AppUser(AbstractBaseUser):
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