from django.test import TestCase
# from .models import Booking
from datetime import datetime
from django.contrib.auth.models import User


class TestViews(TestCase):

    def test_get_booking_list(self):
        response = self.client.get('/reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_list.html')

    def test_get_book_table(self):
        response = self.client.get('/reservations/book_table/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_table.html')
    
    # Need to have test log in
    # def test_get_profile_page(self):
    #     response = self.client.get('/reservations/profile/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'profile.html')
    
    # def test_add_view(self):
    #     self.user = User.objects.create_user(username='testuser', password='12345')
    #     booking = Booking.objects.create('/reservations/book_table/', {first_name='test', last_name='this', number_guests=5, booking_start='2021-12-12 14:00:00', author=self.user})
    #     self.assertRedirects(response, '/reservations/')

    # def test_delete_view(self):
    #     self.user = User.objects.create_user(username='testuser', password='12345')
    #     booking = Booking.objects.create('/reservations/book_table/', {first_name='test', last_name='this', number_guests=5, booking_start=datetime.strptime('2021-12-12 14:00:00', '%Y-%m-%d %H:%M:%S'), author=self.user})
    #     self.assertRedirects(response, '/reservations/')
    #     existing_bookings = Booking.objects.filter(

    #     )
