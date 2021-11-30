from django.test import TestCase


class MainPagesTest(TestCase):
    """
    Test if all bookings pages load
    """

    def test_bookings(self):
        response = self.client.get('/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "booking_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_book_table(self):
        response = self.client.get('/book_table/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_table.html')
        self.assertTemplateUsed(response, "base.html")

    def test_updated_bookings(self):
        response = self.client.get('/updated_bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'updated_bookings.html')
        self.assertTemplateUsed(response, "base.html")

    def test_pending_bookings(self):
        response = self.client.get('/pending_bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_pending.html')
        self.assertTemplateUsed(response, "base.html")


    # def test_manage_appointment(self):
    #     # if user try to enter page not logged in will be redicrect to login
    #     response = self.client.get('/manage-appointment')
    #     self.assertEqual(response.status_code, 301)
