from django.test import TestCase
from .models import Booking
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
    
    def test_get_profile_page(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/reservations/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_update_booking_page(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00',
            slug='xxxxxx')
        response = self.client.get('reservations/xxxxxx/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_update_form.html')

    
    # def test_add_view(self):
    #     self.user = User.objects.create_user(username='testuser', password='12345')
    #     booking = Booking.objects.create('/reservations/book_table/', {first_name='test', last_name='this', number_guests=5, booking_start='2022-12-12 14:00:00', author=self.user})
    #     self.assertRedirects(response, '/reservations/')

    # def test_delete_view(self):
    #     self.user = User.objects.create_user(username='testuser', password='12345')
    #     booking = Booking.objects.create('/reservations/book_table/', {first_name='test', last_name='this', number_guests=5, booking_start=datetime.strptime('2021-12-12 14:00:00', '%Y-%m-%d %H:%M:%S'), author=self.user})
    #     self.assertRedirects(response, '/reservations/')
    #     existing_bookings = Booking.objects.filter(

    #     )
