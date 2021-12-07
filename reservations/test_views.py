from django.test import TestCase
from .models import Booking
from datetime import datetime
from django.contrib.auth.models import User


class TestViews(TestCase):

    def test_get_booking_list(self):
        response = self.client.get('/reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_book_table(self):
        response = self.client.get('/reservations/book_table/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_table.html')
        self.assertTemplateUsed(response, 'base.html')


class TestsLoggedIn(TestCase):
    
    def test_get_profile_page(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/reservations/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertTemplateUsed(response, 'base.html')
    
    def test_get_update_reservation(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')
        response = self.client.get(f'/reservations/{booking.slug}/update/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_update_form.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_cancel_reservation(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')
        response = self.client.get(f'/reservations/{booking.slug}/cancel/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_confirm_delete.html')
        self.assertTemplateUsed(response, 'base.html')

    my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)
    def test_cancel_reservation(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')
        response = self.client.get(f'/reservations/{booking.slug}/cancel/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_confirm_delete.html')
        self.assertTemplateUsed(response, 'base.html')