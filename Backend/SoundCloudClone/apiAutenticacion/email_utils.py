"""
Email utilities for user notifications and communication.

This module provides email services for the SoundCloud clone application,
including welcome emails for new user registrations. The module includes
robust error handling and fallback mechanisms to ensure email delivery
even when encoding issues occur.

Classes:
    EmailService: Static service class for email operations

Features:
    - Welcome email sending for new users
    - Character encoding handling for international names
    - Fallback email system for encoding issues
    - Comprehensive logging for debugging
    - Multiple email backend support (SMTP, console)

Email Backends Supported:
    - SMTP (production): Uses Gmail SMTP for actual email delivery
    - Console (development): Outputs emails to console for testing

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.core.mail import EmailMessage
from django.conf import settings
import logging

# Configure logger for email operations
logger = logging.getLogger(__name__)


class EmailService:
    """
    Service class for handling email operations.
    
    Provides static methods for sending various types of emails to users,
    with robust error handling and fallback mechanisms for encoding issues.
    All email operations are logged for debugging and monitoring purposes.
    
    Methods:
        send_welcome_email(user): Sends welcome email to newly registered users
    
    Design Patterns:
        - Static service class for stateless email operations
        - Fallback pattern for error recovery
        - Template method pattern for email composition
    """
    
    @staticmethod
    def send_welcome_email(user):
        """
        Send a welcome email to a newly registered user.
        
        Creates and sends a personalized welcome email to users who have just
        registered on the platform. Includes information about platform features
        and encourages user engagement. Handles encoding issues gracefully with
        ASCII-only fallback for international characters.
        
        Args:
            user (AppUser): The newly registered user instance containing
                          email, name, and username information
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        
        Features:
            - Personalized message using user's display name
            - Falls back to username if display name has encoding issues
            - ASCII character filtering for international compatibility
            - Fallback to basic email if primary attempt fails
            - Comprehensive error logging for debugging
        
        Email Content:
            - Welcome message with platform introduction
            - List of available features (upload, playlists, follow, discover)
            - Encouraging tone to promote user engagement
            - Professional signature from the team
        
        Error Handling:
            - Primary attempt with full-featured email
            - Secondary attempt with ASCII-only characters
            - Tertiary attempt with basic emergency email
            - All attempts are logged for monitoring
        
        Example:
            user = User.objects.get(email='john@example.com')
            success = EmailService.send_welcome_email(user)
            if success:
                print("Welcome email sent successfully")
            else:
                print("Failed to send welcome email")
        
        Note:
            The method uses EmailMessage for better encoding control compared
            to Django's basic send_mail function. In development with console
            backend, emails are displayed in the terminal instead of sent.
        """
        try:
            # Clean name of special characters for ASCII compatibility
            nombre_limpio = user.nombre.encode('ascii', 'ignore').decode('ascii')
            if not nombre_limpio.strip():
                nombre_limpio = user.username
            
            subject = 'Bienvenido a SoundCloud Clone!'
            
            # Compose personalized welcome message
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
            
            # Clean message of special characters for compatibility
            message_limpio = message.encode('ascii', 'ignore').decode('ascii')
            subject_limpio = subject.encode('ascii', 'ignore').decode('ascii')
            
            # Use EmailMessage for better encoding control
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
            
            # Attempt emergency fallback with basic text only
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
