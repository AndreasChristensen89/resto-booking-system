from django.test import TestCase
from .forms import ContactForm, ContactFormLoggedin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TestBookingForm(TestCase):
    def test_empty_form(self):
        form = ContactForm()
        self.assertFalse(form.is_valid())

    def test_form_with_no_name_field(self):
        form = ContactForm({'name': ''})
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_form_with_no_email_field(self):
        form = ContactForm({
            'name': 'test',
            'email_address': ''
            })
        self.assertIn('email_address', form.errors.keys())
        self.assertEqual(form.errors['email_address'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_form_with_no_message_field(self):
        form = ContactForm({
            'name': 'test',
            'email_address': 'mosh@email.com',
            'message': ''
            })
        self.assertIn('message', form.errors.keys())
        self.assertEqual(form.errors['message'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_form_with_non_email(self):
        form = ContactForm({
            'name': 'name',
            'email_address': 'mosh.com',
            'message': 'Hi'
            })
        self.assertFalse(form.is_valid())


class TestBookingFormLogin(TestCase):
    def test_empty_form(self):
        form = ContactFormLoggedin()
        self.assertFalse(form.is_valid())

    def test_form_with_no_message_field(self):
        form = ContactFormLoggedin({'message': ''})
        self.assertIn('message', form.errors.keys())
        self.assertEqual(form.errors['message'][0], 'This field is required.')
        self.assertFalse(form.is_valid())
