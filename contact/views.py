import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)

class ContactCreateView(APIView):
    """
    API view to receive contact form submissions, validate them, save them to the database,
    and send an email notification to the administrator.
    """
    def post(self, request, *args, **kwargs):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            contact_message = serializer.save()
            
            # Send notification email to the administrator
            self.send_notification_email(contact_message)
            
            return Response(
                {
                    "success": True,
                    "message": "Votre message a bien été envoyé. Nous vous contacterons rapidement."
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def send_notification_email(self, contact_message):
        """
        Sends an email notification to the administrator.
        Fails gracefully if the email server is not configured or throws an error.
        """
        subject = f"[Oyeo Services] Nouveau message de contact - {contact_message.get_service_display()}"
        
        # Prepare context for email templates
        context = {
            'first_name': contact_message.first_name,
            'last_name': contact_message.last_name,
            'email': contact_message.email,
            'phone': contact_message.phone or 'Non renseigné',
            'service': contact_message.get_service_display(),
            'message': contact_message.message,
            'created_at': contact_message.created_at.strftime('%d/%m/%Y %H:%M'),
        }

        # Format a plain text email message
        message_body = (
            f"Bonjour,\n\n"
            f"Vous avez reçu un nouveau message de contact depuis le site Oyeo Services :\n\n"
            f"- Nom complet : {context['first_name']} {context['last_name']}\n"
            f"- Email : {context['email']}\n"
            f"- Téléphone : {context['phone']}\n"
            f"- Prestation souhaitée : {context['service']}\n"
            f"- Date d'envoi : {context['created_at']}\n\n"
            f"Message :\n"
            f"--------------------------------------------------\n"
            f"{context['message']}\n"
            f"--------------------------------------------------\n\n"
            f"Vous pouvez gérer ce message et marquer comme lu depuis l'interface d'administration Django.\n"
        )

        try:
            send_mail(
                subject=subject,
                message=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                fail_silently=False,
            )
            logger.info(f"Notification email sent successfully for contact message ID: {contact_message.id}")
        except Exception as e:
            # We fail silently relative to the API response so the user still gets a success response,
            # but we log the error for backend diagnostics.
            logger.error(f"Failed to send email notification for contact message ID {contact_message.id}: {e}")

