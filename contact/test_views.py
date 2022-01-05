from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from .views import contact


class ContactTest(TestCase):

    def test_contact_page(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contact_page_login(self):
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/contact/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_login.html')
        self.assertTemplateUsed(response, 'base.html')
