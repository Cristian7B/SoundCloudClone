from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_welcome_email(user):
        """
        Envia un email de bienvenida sencillo al usuario recien registrado
        """
        try:
            # Limpiar nombre de caracteres especiales
            nombre_limpio = user.nombre.encode('ascii', 'ignore').decode('ascii')
            if not nombre_limpio.strip():
                nombre_limpio = user.username
            
            subject = 'Bienvenido a SoundCloud Clone!'
            
            message = f"""Hola {nombre_limpio}!

Bienvenido a SoundCloud Clone!

Estamos emocionados de tenerte en nuestra comunidad musical. 

Ya puedes comenzar a:
- Subir tus canciones
- Crear playlists personalizadas
- Seguir a tus artistas favoritos
- Descubrir nueva musica
- Dar like y repostear canciones

Que disfrutes creando y descubriendo musica!

Saludos,
El equipo de SoundCloud Clone"""
            
            # Limpiar mensaje de caracteres especiales
            message_limpio = message.encode('ascii', 'ignore').decode('ascii')
            subject_limpio = subject.encode('ascii', 'ignore').decode('ascii')
            
            # Usar EmailMessage para mejor control de encoding
            email = EmailMessage(
                subject=subject_limpio,
                body=message_limpio,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            
            email.send(fail_silently=False)
            
            logger.info(f"Email de bienvenida enviado a {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email de bienvenida: {str(e)}")
            # Intentar envío de emergencia solo con texto básico
            try:
                from django.core.mail import send_mail
                send_mail(
                    subject='Bienvenido a SoundCloud Clone',
                    message=f'Hola! Bienvenido a SoundCloud Clone. Tu cuenta ha sido creada exitosamente.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                logger.info(f"Email de emergencia enviado a {user.email}")
                return True
            except Exception as e2:
                logger.error(f"Error en email de emergencia: {str(e2)}")
                return False
