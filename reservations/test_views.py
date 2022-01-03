from django.test import TestCase
from .models import Booking, Table
from .forms import BookTableForm
from restaurant.models import OpeningHours, BookingDetails
from datetime import datetime
from django.contrib.auth.models import User
from .test_models import create_booking


class TestsViews(TestCase):

    def test_get_booking_list(self):
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/reservations/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_booking_list_previous(self):
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/reservations/previous_bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_list_previous.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_profile_page(self):
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/reservations/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_password_page(self):
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/reservations/password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_change.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_updated_bookings_page(self):
        my_admin = User.objects.create_superuser('superuser', 'superuser@admin.com', 'adminpass')
        login = self.client.login(username='superuser', password='adminpass')
        response = self.client.get(f'/reservations/updated/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'updated_booking.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_pending_bookings_page(self):
        my_admin = User.objects.create_superuser('superuser', 'superuser@admin.com', 'adminpass')
        login = self.client.login(username='superuser', password='adminpass')
        response = self.client.get(f'/reservations/pending/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pending_bookings.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_update_reservation(self):
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/reservations/{booking.slug}/update/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_update_form.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_cancel_reservation(self):
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/reservations/{booking.slug}/cancel/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_confirm_delete.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_update_booking_admin_page(self):
        my_admin = User.objects.create_superuser('superuser', 'superuser@admin.com', 'adminpass')
        login = self.client.login(username='superuser', password='adminpass')
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        response = self.client.get(f'/reservations/{booking.slug}/update_admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_update_form_admin.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_book_table_view(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        OpeningHours.objects.create(
            weekday=6,
            from_time='10:00',
            to_time='22:00')
        tables = Table.objects.create(
            table_number=2,
            seats=2,
            zone=1,
            )
        BookingDetails.objects.create(
            booking_duration=180,
            table_assign_method=1,
            assign_method_limit=0
        )
        response = self.client.get(f'/reservations/book_table/')
        self.client.post('/reservations/book_table/', {
            'number_guests': 2,
            'booking_start': datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'),
            'comment': 'test',
            })
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.all()[0].number_guests, 2)
        self.assertEqual(Booking.objects.all()[0].comment, 'test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_table.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_approve_reservation(self):
        my_admin = User.objects.create_superuser('superuser', 'superuser@admin.com', 'adminpass')
        login = self.client.login(username='superuser', password='adminpass')
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        response = self.client.get(f'/reservations/{booking.slug}/approve_booking/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_approve_form.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_booking_details(self):
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/reservations/bookings/{booking.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_previous_booking_details(self):
        booking = create_booking('john', datetime.strptime('2020-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get(f'/reservations/previous_bookings/{booking.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_detail_previous.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_available_tables(self):
        my_admin = User.objects.create_superuser('superuser', 'superuser@admin.com', 'adminpass')
        login = self.client.login(username='superuser', password='adminpass')
        booking = create_booking('john', datetime.strptime('4444-11-06 12:00:00', '%Y-%m-%d %H:%M:%S'))
        response = self.client.get(f'/reservations/{booking.slug}/available_tables/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'available_tables.html')
        self.assertTemplateUsed(response, 'base.html')
