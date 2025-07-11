from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailServiceMinimal:
    @staticmethod
    def send_welcome_email(user):
        """
        Version minimalista sin caracteres especiales
        """
        try:
            # Solo usar caracteres ASCII básicos
            nombre = user.username  # Usar username en lugar de nombre
            
            subject = 'Bienvenido a SoundCloud Clone'
            
            message = f"""Hola {nombre}!

Bienvenido a SoundCloud Clone!

Tu cuenta ha sido creada exitosamente.

Ya puedes comenzar a usar la aplicacion.

Saludos,
El equipo de SoundCloud Clone"""
            
            send_mail(
                subject=subject,
                message=message,
                from_email='noreply@soundcloudclone.com',  # Email simple
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            logger.info(f"Email enviado a {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False
