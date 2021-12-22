from django.test import TestCase
from .forms import BookTableForm
from .models import Booking, Table
from restaurant.models import OpeningHours, BookingDetails
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime


def create_booking_form(number_guests):
    """
    creates a booking to shorten test code
    """
    form = BookTableForm({
        'number_guests': number_guests, 
        'booking_start': '2050-12-12 12:00:00',
        'comment': ''
            })
    return form

def create_booking_details(method):
    """
    create booking details to shorten test code
    """
    booking_details = BookingDetails.objects.create(
            booking_duration = 180,
            table_assign_method = method,
            assign_method_limit = 0
        )

    return booking_details


class TestBookingForm(TestCase):
    def test_empty_form(self):
        form = BookTableForm()
        self.assertFalse(form.is_valid())

    def test_form_with_no_guest_number_field(self):
        booking_details = create_booking_details(1)
        form = BookTableForm({'number_guests': ''})
        self.assertIn('number_guests', form.errors.keys())
        self.assertEqual(form.errors['number_guests'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_form_with_no_booking_start_field(self):
        booking_details = create_booking_details(1)
        form = BookTableForm({
            'number_guests': 2, 
            'booking_start': ''
            })
        self.assertIn('booking_start', form.errors.keys())
        self.assertEqual(form.errors['booking_start'][0], 'This field is required.')
        self.assertFalse(form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        form = BookTableForm()
        self.assertEqual(form.Meta.fields, ['number_guests', 'booking_start', 'comment'])

    def test_comment_field_not_required(self):
        opening_hours = OpeningHours.objects.create(
            weekday=0,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            table_number=1,
            seats=4,
            zone=1,
            moveable=True)
        booking_details = create_booking_details(1)
        form = create_booking_form(4)
        self.assertTrue(form.is_valid())

    def test_form_with_minus_integer(self):
        booking_details = create_booking_details(1)
        opening_hours = OpeningHours.objects.create(
            weekday=0,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            table_number=1,
            seats=4,
            zone=1,
            moveable=False
            )
        form = create_booking_form(-1)
        self.assertFalse(form.is_valid())

    def test_zero_tables_available(self):
        booking_details = create_booking_details(1)
        opening_hours = OpeningHours.objects.create(
            weekday=0,
            from_time='10:00', 
            to_time='22:00')
        form = create_booking_form(4)
        self.assertFalse(form.is_valid())

    def test_not_enough_tables_available(self):
        booking_details = create_booking_details(1)
        opening_hours = OpeningHours.objects.create(
            weekday=0,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            table_number=1,
            seats=2,
            zone=1,
            moveable=False
            )
        form = create_booking_form(4)
        self.assertFalse(form.is_valid())

    def test_outside_opening_hours(self):
        booking_details = create_booking_details(1)
        opening_hours = OpeningHours.objects.create(
            weekday=0,
            from_time='21:00', 
            to_time='22:00')
        tables = Table.objects.create(
            table_number=1,
            seats=4,
            zone=1,
            moveable=False
            )
        form = create_booking_form(4)
        self.assertFalse(form.is_valid())

    def test_zero_guests(self):
        booking_details = create_booking_details(1)
        opening_hours = OpeningHours.objects.create(
            weekday=0,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            table_number=1,
            seats=4,
            zone=1,
            moveable=False
            )
        form = create_booking_form(0)
        self.assertFalse(form.is_valid())

    def test_cannot_book_in_past(self):
        opening_hours = OpeningHours.objects.create(
            weekday=5,
            from_time='10:00', 
            to_time='22:00')
        tables = Table.objects.create(
            table_number=1,
            seats=4,
            zone=1,
            moveable=True)
        booking_details = create_booking_details(1)
        form = BookTableForm({
        'number_guests': 2, 
        'booking_start': '2020-12-12 12:00:00',
        'comment': ''
            })
        self.assertFalse(form.is_valid())
