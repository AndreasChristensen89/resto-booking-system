from django.test import TestCase
from .forms import BookTableForm
from django.contrib.auth.models import User


class TestBookingForm(TestCase):
    # there seems to be problems testing this since I'm using functions inside the form function
    # If i remove the functions the test passes
    def test_empty_form(self):
        form = BookTableForm()
        self.assertFalse(form.is_valid())

    def test_form_with_no_first_name_field(self):
        form = BookTableForm({'first_name': ''})
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(form.errors['first_name'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_form_with_no_last_name_field(self):
        form = BookTableForm({'first_name': 'x', 'last_name': ''})
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(form.errors['last_name'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_form_with_no_guest_number_field(self):
        form = BookTableForm({'first_name': 'x', 'last_name': 'x', 'number_guests': ''})
        self.assertIn('number_guests', form.errors.keys())
        self.assertEqual(form.errors['number_guests'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_form_with_no_booking_start_field(self):
        form = BookTableForm({
            'first_name': 'x', 
            'last_name': 'x', 
            'number_guests': 2, 
            'booking_start': ''
            })
        self.assertIn('booking_start', form.errors.keys())
        self.assertEqual(form.errors['booking_start'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = BookTableForm()
        self.assertEqual(form.Meta.fields, ['first_name', 'last_name', 'number_guests', 'booking_start', 'comment'])

    def test_comment_field_not_required(self):
        form = BookTableForm({
                'first_name': 'x',
                'last_name': 'x',
                'number_guests': 4,
                'booking_start': '2021-12-12 13:00:00',
                'comment': 'test'
                })
        self.assertTrue(form.is_valid())