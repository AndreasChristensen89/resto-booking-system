from django.test import TestCase
from .models import Booking, Table
from django.contrib.auth.models import User
from .booking import return_tables, double_booking
from restaurant.models import BookingDetails
from datetime import datetime, timedelta

def create_booking(name, date):
    user = User.objects.create_user(name, 'lennon@thebeatles.com', 'johnpassword')
    booking = Booking.objects.create(
        author=user, 
        number_guests=4, 
        booking_start=date+' 12:00:00',
        booking_end=date+' 15:00:00')
    return booking


class TestModels(TestCase):
    
    def test_object_exists(self):
        booking = create_booking('john', '4444-11-06')
        self.assertEqual(len(Booking.objects.filter(booking_start='4444-11-06 12:00:00')), 1)
    
    def test_pending_status_is_zero(self):
        booking = create_booking('john', '4444-11-06')
        self.assertEqual(booking.status, 0)
    
    def test_booking_slug_are_generated_and_unique(self):
        booking1 = create_booking('john', '4444-11-06')
        booking2 = create_booking('paul', '3333-11-06')
        self.assertEqual(len(str(booking1.slug)), 5)
        self.assertEqual(len(str(booking2.slug)), 5)
        self.assertNotEqual(booking1.slug, booking2.slug)

    def test_model_property_is_past_due(self):
        booking1 = create_booking('john', '4444-11-06')
        booking2 = create_booking('paul', '2020-11-06')
        self.assertEqual(booking1.is_past_due, False)
        self.assertEqual(booking2.is_past_due, True)

    def test_model_property_latest_cancellation(self):
        """
        Creates two bookings:
        One is in 60 minutes, the other is 121 minutes away
        60 minutes away is too late (False), 121 minutes is just in time (True)
        """
        in_an_hour = datetime.now().replace(microsecond=0) + timedelta(minutes=60)
        date_str = str(in_an_hour)
        date_end_str = str(in_an_hour + timedelta(minutes=180))

        user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        booking1 = Booking.objects.create(
        author=user1, 
        number_guests=4, 
        booking_start=date_str,
        booking_end=date_end_str)

        booking_hours_away = in_an_hour + timedelta(minutes=61)
        booking_hours_away_str = str(booking_hours_away)
        booking_hours_away_end_str = str(booking_hours_away + timedelta(minutes=180))

        user2 = User.objects.create_user('paul', 'mccartney@thebeatles.com', 'paulpassword')
        booking2 = Booking.objects.create(
        author=user2, 
        number_guests=4, 
        booking_start=booking_hours_away_str,
        booking_end=booking_hours_away_end_str)

        self.assertEqual(booking1.latest_cancellation, False)
        self.assertEqual(booking2.latest_cancellation, True)
