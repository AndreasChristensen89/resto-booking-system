from django.test import TestCase
from .models import Booking, Table
from django.contrib.auth.models import User
from .booking import return_tables, double_booking
from restaurant.models import BookingDetails

def create_booking():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    booking = Booking.objects.create(
        first_name='x',
        last_name='x', 
        author=user, 
        number_guests=4, 
        booking_start='4444-11-06 12:00:00',
        booking_end='4444-11-06 15:00:00')
    return booking


class TestModels(TestCase):
    
    def test_object_exists(self):
        booking = create_booking()
        self.assertEqual(len(Booking.objects.filter(booking_start='4444-11-06 12:00:00')), 1)
    
    def test_pending_status_is_zero(self):
        booking = create_booking()
        self.assertEqual(booking.status, 0)
    
    def test_booking_slug(self):
        booking = create_booking()
        self.assertEqual(str(booking.slug)[0:2], 'xx')
        self.assertEqual(len(str(booking.slug)[2:]), 4)