from django.test import TestCase

class TestViews(TestCase):

    def test_get_booking_list(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_list.html')

    # def test_get_book_table(self):
    #     response = self.client.get('/reservations/book_table/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'book_table.html')