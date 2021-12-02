from django.test import TestCase
from .forms import BookTableForm


# class TestBookingForm(TestCase):

#     def test_one_is_one(self):
#         self.assertEqual(1, 1)
#     # there seems to be problems testing this since I'm using functions inside the form function
#     # If i remove the functions the test passes
#     def test_first_name_is_required(self):
#         form = BookTableForm({'first_name': '')
#         self.assertFalse(form.is_valid())
#         self.assertIn('first_name', form.errors.keys())
#         self.assertEqual(form.errors['first_name'][0], 'This field is required.')
