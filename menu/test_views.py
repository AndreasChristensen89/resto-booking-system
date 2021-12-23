from django.test import TestCase

class TestViews(TestCase):

    def test_get_menu_list(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_list.html')
        self.assertTemplateUsed(response, 'base.html')
