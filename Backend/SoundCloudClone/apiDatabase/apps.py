from django.apps import AppConfig


class ApidatabaseConfig(AppConfig):
    """
    Clase para configurar el microservicio de base de datos.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apiDatabase'
