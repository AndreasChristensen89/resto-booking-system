from django.test import TestCase
from .forms import BookTableForm
from .models import Booking, Table
from restaurant.models import OpeningHours, BookingDetails
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime


def create_booking_form(number_guests):
    form = BookTableForm({
        'first_name': 'x', 
        'last_name': 'x', 
        'number_guests': number_guests, 
        'booking_start': '2021-12-12 12:00:00',
        'comment': ''
            })
    return form


class TestBookingForm(TestCase):
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
        opening_hours = OpeningHours.objects.create(
            weekday=6,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            size=4)
        BookingDetails.objects.create(booking_duration=180, auto_table_assign=True)
        form = create_booking_form(4)
        self.assertTrue(form.is_valid())

    def test_form_with_minus_integer(self):
        opening_hours = OpeningHours.objects.create(
            weekday=6,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            size=4)
        form = create_booking_form(-1)
        self.assertRaises(ValidationError)

    def test_zero_tables_available(self):
        opening_hours = OpeningHours.objects.create(
            weekday=6,
            from_time='10:00', 
            to_time='22:00')
        form = create_booking_form(4)
        self.assertRaises(ValidationError)

    def test_not_enough_tables_available(self):
        opening_hours = OpeningHours.objects.create(
            weekday=6,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            size=2)
        form = create_booking_form(4)
        self.assertRaises(ValidationError)

    def test_outside_opening_hours(self):
        opening_hours = OpeningHours.objects.create(
            weekday=6,
            from_time='13:00', 
            to_time='22:00')
        tables = Table.objects.create(
            size=4)
        form = create_booking_form(4)
        self.assertRaises(ValidationError)

    def test_outside_zero_guests(self):
        opening_hours = OpeningHours.objects.create(
            weekday=6,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            size=4)
        form = create_booking_form(0)
        self.assertRaises(ValidationError)
