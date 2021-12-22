from django.test import TestCase
from django.core import mail
from .views import contact


class ContacTest(TestCase):
    
    def test_send_email(self):
        mail.send_mail('Test subject', 'Test message',
                       'from@example.com', ['to@example.com'],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test subject')
        self.assertEqual(mail.outbox[0].body, 'Test message')
        self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
        self.assertEqual(mail.outbox[0].to, ['to@example.com'])