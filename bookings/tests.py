from django.test import TestCase


class TestBookingPages(TestCase):
    """
    Test if all bookings pages load
    """

    def test_bookings(self):
        response = self.client.get('/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "booking_list.html")
        self.assertTemplateUsed(response, "base.html")

    # def test_book_table(self):
    #     response = self.client.get('bookings/book_table')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'book_table.html')
    #     self.assertTemplateUsed(response, "base.html")
