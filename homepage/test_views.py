from django.test import TestCase


class TestViews(TestCase):

    def test_homepage_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_404_page(self):
        response = self.client.get('/asdsadsadsad/Asdsad')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')
        self.assertTemplateUsed(response, 'base.html')
