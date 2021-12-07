from django.test import TestCase
from .models import Booking
from django.contrib.auth.models import User


class TestModels(TestCase):

    def test_booking_end_is_generated(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        booking = Booking.objects.create(first_name='x', last_name='x', author=user, number_guests=4, booking_start='2021-11-06 12:00:00')
        self.assertTrue(booking.booking_end, '2021-11-06 15:00:00')
    
    def test_pending_status_is_zero(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        booking = Booking.objects.create(first_name='x', last_name='x', author=user, number_guests=2, booking_start='2021-12-28 13:00:00')
        self.assertEqual(booking.status, 0)
