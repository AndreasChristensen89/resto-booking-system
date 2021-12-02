from django.test import TestCase
from .models import Booking


class TestViews(TestCase):

    def test_get_booking_list(self):
        response = self.client.get('/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_list.html')

    def test_get_book_table(self):
        response = self.client.get('/bookings/book_table/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_table.html')

    # def test_get_profile_page(self):
    #     response = self.client.get('/bookings/profile/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'profile.html')
    
    def test_update_view(self):
        booking = Booking.objects.create(first_name='test', last_name='this', number_guests=5, booking_start='2021-12-12 14:00')
        response = self.client.get(f'/bookings/{booking.id}/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_update_form.html')

    # def test_delete_view(self):

