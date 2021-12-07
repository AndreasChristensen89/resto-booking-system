from django.test import TestCase
from .models import Booking
from django.contrib.auth.models import User
from .booking import return_tables, double_booking
from restaurant.models import BookingDetails


class TestModels(TestCase):

    # def test_booking_end_is_generated(self):
    #     user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    #     booking = Booking.objects.create(
    #         first_name='x',
    #         last_name='x', 
    #         author=user, 
    #         number_guests=4, 
    #         booking_start='2021-11-06 12:00:00',
    #         booking_end='2021-11-06 15:00:00')
    #     self.assertEqual(booking.booking_end, '2021-11-06 15:00:00')
    
    def test_pending_status_is_zero(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')
        self.assertEqual(booking.status, 0)

    # def test_user_is_same(self):
    #     user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    #     booking = Booking.objects.create(
    #         first_name='x',
    #         last_name='x', 
    #         author=user, 
    #         number_guests=4, 
    #         booking_start='2021-11-06 12:00:00',
    #         booking_end='2021-11-06 15:00:00')
    #     self.assertEqual(booking.author.username, 'john')

    # tables are added after the second save in views, therefore test shows tables as []
    # def test_tables_empty(self):
    #     user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    #     booking = Booking.objects.create(
    #         first_name='x',
    #         last_name='x', 
    #         author=user, 
    #         number_guests=4, 
    #         booking_start='2021-11-06 12:00:00',
    #         booking_end='2021-11-06 15:00:00')
    #     self.assertEqual(len(booking.table.all()), 0)
    
    def test_booking_slug(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')
        self.assertEqual(str(booking.slug)[0:2], 'xx')
        self.assertEqual(len(str(booking.slug)[2:]), 4)
        
