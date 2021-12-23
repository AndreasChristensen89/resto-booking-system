from django.test import TestCase
from .models import Booking, Table
from django.contrib.auth.models import User
from .booking import return_tables, double_booking
from restaurant.models import BookingDetails
from datetime import datetime, timedelta

def create_booking(name, datetime):
    user = User.objects.create_user(name, 'lennon@thebeatles.com', 'johnpassword')
    booking = Booking.objects.create(
        author=user, 
        number_guests=4, 
        booking_start=datetime,
        booking_end=datetime+timedelta(minutes=180))
    return booking


class TestModels(TestCase):
    """
    In TestCase the string in datetimefield is not converted to datetime
    Therefore I'm inserting datetime in booking_start/end instead of a string.
    If not, properties cannot be tested due to errors with timedelta
    """
    def test_object_exists(self):
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(len(Booking.objects.filter(booking_start='4444-11-06 12:00:00')), 1)
    
    def test_pending_status_is_zero(self):
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(booking.status, 0)
    
    def test_booking_slug_are_generated_and_unique(self):
        booking1 = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        booking2 = create_booking('paul', datetime.strptime('3333-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(len(str(booking1.slug)), 5)
        self.assertEqual(len(str(booking2.slug)), 5)
        self.assertNotEqual(booking1.slug, booking2.slug)

    def test_model_property_is_past_due(self):
        booking1 = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        booking2 = create_booking('paul', datetime.strptime('2020-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(booking1.is_past_due, False)
        self.assertEqual(booking2.is_past_due, True)

    def test_model_property_latest_cancellation(self):
        in_an_hour = datetime.now().replace(microsecond=0) + timedelta(minutes=60)
        booking1 = create_booking('john', in_an_hour)

        booking_in_time = in_an_hour + timedelta(minutes=61)
        booking2 = create_booking('paul', booking_in_time)

        self.assertEqual(booking1.latest_cancellation, False)
        self.assertEqual(booking2.latest_cancellation, True)
