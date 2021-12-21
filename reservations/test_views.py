from django.test import TestCase
from .models import Booking, Table
from .forms import BookTableForm
from restaurant.models import OpeningHours, BookingDetails
from datetime import datetime
from django.contrib.auth.models import User
from .test_models import create_booking


class TestViews(TestCase):

    def test_get_book_table(self):
        response = self.client.get('/reservations/book_table/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_table.html')
        self.assertTemplateUsed(response, 'base.html')

    # path('profile/', views.ProfileView.as_view(), name='profile'), DONE
    # path('password/', views.PasswordChangeView.as_view(), name='password'),
    # path('resetpassword/', views.PasswordChangeView.as_view(), name='password'),
    # path('', views.BookingList.as_view(), name='booking_list'), DONE
    # path('book_table/', views.book_table, name='book_table'), DONE
    # path('updated/', views.BookingUpdated.as_view(), name='bookings_updated'), DONE
    # path('pending/', views.BookingPending.as_view(), name='bookings_pending'), DONE
    # path('<slug:slug>/', views.BookingDetail.as_view(), name='booking_detail'),
    # path('<slug:slug>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'), DONE
    # path('<slug:slug>/update/', views.UpdateReservationView.as_view(), name='update_booking'), DONE
    # path('<slug:slug>/update_admin/', views.UpdateReservationViewAdmin.as_view(), name='admin_update_booking'),
    # path('<slug:slug>/approve_booking/', views.ApproveReservationViewAdmin.as_view(), name='approve_booking'),


class TestsLoggedIn(TestCase):
    
    def test_get_booking_list(self):
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        login = self.client.login(username='john', password='johnpassword')
        response = self.client.get('/reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_list.html')
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
        self.client.login(username='john', password='johnpassword')
        booking = create_booking()
        response = self.client.get(f'/reservations/{booking.slug}/update/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_update_form.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_update_reservation(self):
        self.client.login(username='john', password='johnpassword')
        booking = create_booking()
        response = self.client.get(f'/reservations/{booking.slug}/update/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_update_form.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_cancel_reservation(self):
        self.client.login(username='john', password='johnpassword')
        booking = create_booking()
        response = self.client.get(f'/reservations/{booking.slug}/cancel/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_confirm_delete.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_get_update_booking_admin_page(self):
        my_admin = User.objects.create_superuser('superuser', 'superuser@admin.com', 'adminpass')
        login = self.client.login(username='superuser', password='adminpass')
        booking = create_booking()
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
            table_number=1,
            seats=2,
            zone=1,
            moveable=False
            )
        tables = Table.objects.create(
            table_number=2,
            seats=2,
            zone=1,
            moveable=False
            )
        BookingDetails.objects.create(
            booking_duration=180,
            table_assign_method=1,
            assign_method_limit=0
        )
        self.client.post('/reservations/book_table/', {
            'number_guests': 4, 
            'booking_start': '2021-12-12 12:00:00',
            'comment': 'test',
            })
        all_bookings = Booking.objects.all()
        self.assertEqual(all_bookings[0].number_guests, 4)
        self.assertEqual(all_bookings[0].comment, 'test')
        # Book.objects.count()
        
    # test limit