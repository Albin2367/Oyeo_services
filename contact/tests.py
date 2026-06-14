from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ContactMessage

class ContactAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('contact-submit')
        self.valid_payload = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean.dupont@example.com',
            'phone': '0612345678',
            'service': 'menage',
            'message': 'Bonjour, je souhaiterais obtenir un devis pour 2h de ménage par semaine.'
        }

    def test_contact_submission_success(self):
        """
        Ensure a valid contact form submission successfully saves to the database
        and sends a notification email.
        """
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        # Verify status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        
        # Verify database save
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.first()
        self.assertEqual(message.first_name, 'Jean')
        self.assertEqual(message.last_name, 'Dupont')
        self.assertEqual(message.email, 'jean.dupont@example.com')
        self.assertEqual(message.service, 'menage')
        
        # Verify email outbox contains the sent notification
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertIn("[Oyeo Services] Nouveau message de contact", sent_email.subject)
        self.assertIn("Jean Dupont", sent_email.body)
        self.assertIn("Ménage / Repassage", sent_email.body)

    def test_contact_submission_missing_fields(self):
        """
        Ensure submission fails if required fields are missing.
        """
        incomplete_payload = {
            'first_name': 'Jean',
            # missing last_name, email, message
        }
        response = self.client.post(self.url, incomplete_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('last_name', response.data['errors'])
        self.assertIn('email', response.data['errors'])
        self.assertIn('message', response.data['errors'])
        
        # Check database remains empty
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_submission_invalid_email(self):
        """
        Ensure submission fails if email format is invalid.
        """
        invalid_email_payload = self.valid_payload.copy()
        invalid_email_payload['email'] = 'not-an-email'
        
        response = self.client.post(self.url, invalid_email_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors'])
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_submission_invalid_service_choice(self):
        """
        Ensure submission fails if the service choice is invalid.
        """
        invalid_service_payload = self.valid_payload.copy()
        invalid_service_payload['service'] = 'invalid-choice'
        
        response = self.client.post(self.url, invalid_service_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('service', response.data['errors'])
        self.assertEqual(ContactMessage.objects.count(), 0)

