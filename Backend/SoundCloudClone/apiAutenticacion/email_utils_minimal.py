"""
Minimal email utilities for user notifications (ASCII-only fallback).

This module provides a simplified email service implementation that uses only
ASCII characters to avoid encoding issues in environments with limited
character set support. Serves as a fallback when the main email service
encounters encoding problems.

Classes:
    EmailServiceMinimal: Simplified email service with ASCII-only content

Features:
    - ASCII-only email content to prevent encoding issues
    - Simplified message templates for maximum compatibility
    - Robust error handling with comprehensive logging
    - Fallback solution for international character problems

Use Cases:
    - Fallback when main email service fails due to encoding
    - Environments with limited character set support
    - Legacy systems requiring ASCII-only content
    - Testing scenarios with simple text requirements

@author: Development Team
@version: 1.0
@since: 2024
"""

from django.core.mail import send_mail
from django.conf import settings
import logging

# Configure logger for minimal email operations
logger = logging.getLogger(__name__)


class EmailServiceMinimal:
    """
    Minimal email service implementation with ASCII-only content.
    
    Provides basic email functionality using only ASCII characters to ensure
    maximum compatibility across different email systems and environments.
    Designed as a fallback solution when the main email service encounters
    encoding issues with international characters.
    
    Methods:
        send_welcome_email(user): Send ASCII-only welcome email to new users
    
    Design Philosophy:
        - Simplicity over features for maximum reliability
        - ASCII-only content to prevent encoding issues
        - Minimal dependencies for broad compatibility
        - Clear error logging for troubleshooting
    """
    
    @staticmethod
    def send_welcome_email(user):
        """
        Send a minimal welcome email using only ASCII characters.
        
        Creates and sends a simple welcome email to newly registered users
        using only ASCII characters to avoid encoding issues. Uses the user's
        username instead of display name to ensure ASCII compatibility.
        
        Args:
            user (AppUser): The newly registered user instance
        
        Returns:
            bool: True if email was sent successfully, False otherwise
        
        Features:
            - ASCII-only content for maximum compatibility
            - Uses username instead of potentially non-ASCII display name
            - Simple Django send_mail function for reliability
            - Comprehensive error logging for debugging
        
        Email Content:
            - Basic welcome message
            - Account creation confirmation
            - Simple application introduction
            - Professional team signature
        
        Error Handling:
            - Logs successful email delivery
            - Captures and logs any exceptions
            - Returns boolean status for calling code
        
        Example:
            user = User.objects.get(email='john@example.com')
            success = EmailServiceMinimal.send_welcome_email(user)
            if success:
                print("Minimal welcome email sent")
            else:
                print("Failed to send minimal email")
        
        Note:
            This method is designed as a fallback when the main email service
            fails due to encoding issues. It sacrifices features for reliability.
        """
        try:
            # Use username to ensure ASCII compatibility
            nombre = user.username  
            
            # ASCII-only subject line
            subject = 'Bienvenido a SoundCloud Clone'
            
            # Simple ASCII-only message template
            message = f"""Hola {nombre}!

Bienvenido a SoundCloud Clone!

Tu cuenta ha sido creada exitosamente.

Ya puedes comenzar a usar la aplicacion.

Saludos,
El equipo de SoundCloud Clone"""
            
            # Send email using Django's basic send_mail function
            send_mail(
                subject=subject,
                message=message,
                from_email='noreply@soundcloudclone.com',  # Fixed sender for simplicity
                recipient_list=[user.email],
                fail_silently=False,  # Raise exceptions for debugging
            )
            
            logger.info(f"Email enviado a {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return False
